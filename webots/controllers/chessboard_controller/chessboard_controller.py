from controller import Supervisor, Keyboard
import math

TIME_STEP = 32
BOARD_SIZE = 8
SQUARE = 0.5
BOARD_ORIGIN_X = -(BOARD_SIZE * SQUARE) / 2 + SQUARE / 2
BOARD_ORIGIN_Y = -(BOARD_SIZE * SQUARE) / 2 + SQUARE / 2
PIECE_Z = 0.20
CARRIAGE_Z = 0.08


def square_position(square, z=PIECE_Z):
    file_idx = ord(square[0]) - ord('a')
    rank_idx = int(square[1]) - 1
    return [BOARD_ORIGIN_X + file_idx * SQUARE,
            BOARD_ORIGIN_Y + rank_idx * SQUARE,
            z]


class ChessboardMVP:
    def __init__(self):
        self.robot = Supervisor()
        self.keyboard = Keyboard()
        self.keyboard.enable(TIME_STEP)
        self.root = self.robot.getRoot().getField('children')
        self.pieces = {}
        self.carriage = self.robot.getFromDef('CARRIAGE')
        self.magnet = self.robot.getFromDef('MAGNET')
        self.status = self.robot.getFromDef('STATUS')
        self.animating = False
        self.animation = None
        self.human_move_done = False
        self.demo_done = False

    def piece_node(self, square):
        return self.robot.getFromDef('P_' + square.upper())

    def move_piece(self, from_sq, to_sq, duration=1.2):
        piece = self.piece_node(from_sq)
        if piece is None:
            return False
        start = square_position(from_sq)
        end = square_position(to_sq)
        self.animation = {
            'piece': piece,
            'from': from_sq,
            'to': to_sq,
            'start': start,
            'end': end,
            'elapsed': 0.0,
            'duration': duration,
        }
        self.animating = True
        self.set_status('ROBOT MOVING', f'{from_sq} → {to_sq}')
        return True

    def animate(self, dt):
        if not self.animating:
            return
        a = self.animation
        a['elapsed'] += dt
        t = min(1.0, a['elapsed'] / a['duration'])
        # Smooth trapezoid-like easing for a convincing robot motion.
        e = t * t * (3.0 - 2.0 * t)
        x = a['start'][0] + (a['end'][0] - a['start'][0]) * e
        y = a['start'][1] + (a['end'][1] - a['start'][1]) * e
        z = PIECE_Z + 0.04 * math.sin(math.pi * t)
        a['piece'].getField('translation').setSFVec3f([x, y, z])

        # The carriage follows the piece underneath it.
        self.carriage.getField('translation').setSFVec3f([x, y, CARRIAGE_Z])
        self.magnet.getField('translation').setSFVec3f([x, y, 0.145])

        if t >= 1.0:
            self.animating = False
            self.set_status('READY', f'Completed {a["from"]} → {a["to"]}')

    def set_status(self, title, detail):
        if self.status:
            self.status.getField('name').setSFString(f'{title}: {detail}')
        print(f'[CHESS] {title}: {detail}')

    def human_move(self):
        if self.animating or self.human_move_done:
            return
        piece = self.piece_node('e2')
        if piece is None:
            return
        # Human movement is represented as an instantaneous sensor event.
        piece.getField('translation').setSFVec3f(square_position('e4'))
        self.human_move_done = True
        self.set_status('SENSOR EVENT', 'Human move detected: e2 → e4')

    def ai_move(self):
        if self.animating or not self.human_move_done or self.demo_done:
            return
        self.demo_done = True
        self.move_piece('e7', 'e5')

    def reset(self):
        for sq in ('e2', 'e7'):
            p = self.piece_node(sq)
            if p:
                p.getField('translation').setSFVec3f(square_position(sq))
        # e4 is the same physical node as e2; restoring e2 is enough.
        self.human_move_done = False
        self.demo_done = False
        self.animating = False
        self.animation = None
        self.carriage.getField('translation').setSFVec3f([0, 0, CARRIAGE_Z])
        self.magnet.getField('translation').setSFVec3f([0, 0, 0.145])
        self.set_status('READY', 'Waiting for human move')

    def run(self):
        self.set_status('READY', 'Press 1 for e2-e4 + AI response, D for demo, R to reset')
        while self.robot.step(TIME_STEP) != -1:
            key = self.keyboard.getKey()
            if key in (ord('1'), ord('1') + 32):
                self.human_move()
                if self.human_move_done and not self.animating:
                    # Schedule AI response on the next control cycle.
                    self.ai_move()
            elif key in (ord('d'), ord('D')):
                if not self.animating:
                    self.human_move_done = True
                    self.ai_move()
            elif key in (ord('r'), ord('R')):
                self.reset()
            self.animate(TIME_STEP / 1000.0)


if __name__ == '__main__':
    ChessboardMVP().run()
