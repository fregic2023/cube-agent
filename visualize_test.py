# %%
import numpy as np
import math
import copy

# %%
notation_dict = {'': 1, '2': 2, "'": 3}
notation_dict_reverse = {1: '', 2: '2', 3: "'"}

class Axis:
    x = 0
    y = 1
    z = 2
    _x = 3
    _y = 4
    _z = 5

    @staticmethod
    def plane_rotation(x, y, angle):
        cos = int(math.cos(angle))
        sin = int(math.sin(angle))

        _x = cos*x + sin*y
        _y = - sin*x + cos*y
        return _x, _y


class Position:
    zero = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, position):
        return Position(self.x+position.x, self.y+position.y, self.z+position.z)

    def __sub__(self, position):
        return Position(self.x-position.x, self.y-position.y, self.z-position.z)

    def __neg__(self):
        return Position(-self.x, -self.y, -self.z)

    def __eq__(self, position):
        return self.x == position.x and self.y == position.y and self.z == position.z

    def __str__(self):
        return f"[x: {self.x}, y: {self.y}, z: {self.z}]"

    def copy(self):
        return Position(self.x, self.y, self.z)

    def rotate_around_axis(self, axis: int, angle):
        if axis == Axis.x:
            self.y, self.z = Axis.plane_rotation(self.y, self.z, angle)
        elif axis == Axis.y:
            self.z, self.x = Axis.plane_rotation(self.z, self.x, angle)
        elif axis == Axis.z:
            self.x, self.y = Axis.plane_rotation(self.x, self.y, angle)
        if axis == Axis._x:
            self.z, self.y = Axis.plane_rotation(self.z, self.y, angle)
        elif axis == Axis._y:
            self.x, self.z = Axis.plane_rotation(self.x, self.z, angle)
        elif axis == Axis._z:
            self.y, self.x = Axis.plane_rotation(self.y, self.x, angle)
        else:
            return None


Position.zero = Position(0, 0, 0)


# %% 
class Face:
    def __init__(self, name: str, color: str, dir: Position):
        self.name = name
        self.color = color
        self.dir = dir


class Faces:
    face_R = Face(name='R', color='R', dir=Position(1, 0, 0))
    face_U = Face(name='U', color='W', dir=Position(0, 1, 0))
    face_F = Face(name='F', color='G', dir=Position(0, 0, 1))
    face_L = Face(name='L', color='O', dir=Position(-1, 0, 0))
    face_D = Face(name='D', color='Y', dir=Position(0, -1, 0))
    face_B = Face(name='B', color='B', dir=Position(0, 0, -1))

    face_count = 6
    face_array = [face_R, face_U, face_F, face_L, face_D, face_B]

    color_to_int = {face_R.color:1,face_U.color:2,face_F.color:3,face_L.color:4,face_D.color:5,face_B.color:6,None:0}

    @staticmethod
    def get_index_by_dir(dir):
        for i,face in enumerate(Faces.face_array):
            if face.dir == dir:
                return i
        return None

    @staticmethod
    def get_face_by_name(face_name: str):
        for face in Faces.face_array:
            if face.name == face_name:
                return face
        return None


# %%
class Piece:
    def __init__(self, pos: Position):
        self.color = []
        self.pos = pos
        self.dir_R = Faces.face_R.dir.copy()
        self.dir_U = Faces.face_U.dir.copy()
        self.dir_F = Faces.face_F.dir.copy()

    def __str__(self):
        return f"[pos: {self.pos}, dir_R: {self.dir_R}, dir_U: {self.dir_U}, colors: {self.color}]"

    def rotate_around_axis(self, axis: int, angle):
        self.pos.rotate_around_axis(axis, angle)
        self.dir_R.rotate_around_axis(axis, angle)
        self.dir_U.rotate_around_axis(axis, angle)
        self.dir_F.rotate_around_axis(axis, angle)

    def dir_color(self, dir):
        if self.dir_R == dir:
            return self.color[0]
        if self.dir_U == dir:
            return self.color[1]
        if self.dir_F == dir:
            return self.color[2]
        if -self.dir_R == dir:
            return self.color[3]
        if -self.dir_U == dir:
            return self.color[4]
        if -self.dir_F == dir:
            return self.color[5]
        print(">>> " + str(dir))
        return None

class Piece_holder:
    def __init__(self, piece: Piece):
        self.pos = piece.pos.copy()
        self.piece = piece


class Layer:
    def __init__(self, name: str, axis: int, turn_angle, piece_holder_array: list[Piece_holder]):
        self.name = name
        self.axis = axis
        self.turn_angle = turn_angle
        self.piece_holder_array = piece_holder_array

    def add_holder(self,piece_holder: Piece_holder):
        self.piece_holder_array.append(piece_holder)

    def get_holder_by_pos(self, pos):
        for holder in self.piece_holder_array:
            if holder.pos == pos:
                return holder
        return None

    def turn(self, turns):
        piece_array = []

        for holder in self.piece_holder_array:
            holder.piece.rotate_around_axis(self.axis, self.turn_angle * turns)
            #piece_array.append(copy.deepcopy(holder.piece))
            piece_array.append(holder.piece)
            holder.piece = None

        for piece in piece_array:
            holder = self.get_holder_by_pos(piece.pos)
            if holder == None:
                print("holder == none???")
                continue
            if holder.piece != None:
                print('piece != none???')
                continue
            holder.piece = piece


# %%
class Layer_dimension:
    def __init__(self, axis: int, layer_info: []):
        self.axis = axis
        self.layer_info = layer_info

# %%
class Cube:
    def __init__(self, name: str):

        if name =='2x2x2':
            self.size = 2
            turn_angle = math.pi/2
            xLayers = Layer_dimension(Axis.x, [ ['R', Axis.x, turn_angle, 0.5], ['L', Axis._x, turn_angle, -0.5] ])
            yLayers = Layer_dimension(Axis.y, [ ['U', Axis.y, turn_angle, 0.5], ['D', Axis._y, turn_angle, -0.5] ])
            zLayers = Layer_dimension(Axis.z, [ ['F', Axis.z, turn_angle, 0.5], ['B', Axis._z, turn_angle, -0.5] ])
            layer_dimension_array = [xLayers,yLayers,zLayers]
        if name == '3x3x3':
            self.size = 3
            turn_angle = math.pi/2
            xLayers = Layer_dimension(Axis.x, [ ['R', Axis.x, turn_angle, 1], ['M', Axis._x, turn_angle, 0], ['L', Axis._x, turn_angle, -1] ])
            yLayers = Layer_dimension(Axis.y, [ ['U', Axis.y, turn_angle, 1], ['E', Axis._y, turn_angle, 0], ['D', Axis._y, turn_angle, -1] ])
            zLayers = Layer_dimension(Axis.z, [ ['F', Axis.z, turn_angle, 1], ['S', Axis.z , turn_angle, 0], ['B', Axis._z, turn_angle, -1] ])
            layer_dimension_array = [xLayers,yLayers,zLayers]

        self.piece_holder_array = []
        self.layer_array = []
        
        self.generate(layer_dimension_array)
        self.link()

    def get_holder_by_pos(self, holder_pos) -> Piece_holder:
        for holder in self.piece_holder_array:
            if holder.pos == holder_pos:
                return holder
        return None

    def get_layer_by_name(self, layer_name) -> Layer:
        for layer in self.layer_array:
            if layer.name == layer_name:
                return layer
        print("Layer nonexistent: Cube_3x3x3.get_layer_by_name")
        return None

    def generate(self,layer_dimension_array):
        name = 0
        axis = 1
        turn_angle = 2
        position = 3

        for layer_dimension in layer_dimension_array:
            for layer_info in layer_dimension.layer_info:
                layer = Layer(layer_info[name],layer_info[axis],layer_info[turn_angle],[])
                self.layer_array.append(layer)
                #print(f'layer {layer.name} generated')

        xLayers = layer_dimension_array[0]
        yLayers = layer_dimension_array[1]
        zLayers = layer_dimension_array[2]

        for x in xLayers.layer_info:
            for y in yLayers.layer_info:
                for z in zLayers.layer_info:
                    piece = Piece(Position(x[position], y[position], z[position]))
                    holder = Piece_holder(piece)
                    self.piece_holder_array.append(holder)
                    
                    self.get_layer_by_name(x[name]).add_holder(holder)
                    self.get_layer_by_name(y[name]).add_holder(holder)
                    self.get_layer_by_name(z[name]).add_holder(holder)
                    # print(f'piece&holder {x[name]}{y[name]}{z[name]} generated at {piece.pos}')
        
    def link(self):
        for holder in self.piece_holder_array:
            for face in Faces.face_array:
                adjacent_holder = self.get_holder_by_pos(holder.pos+face.dir)

                if adjacent_holder != None:  # a piece exists in the given direction
                    holder.piece.color.append(None)
                else:  # colored side or internal piece
                    holder.piece.color.append(face.color)

    def turn(self, layer_name: str, turns: int):
        layer = self.get_layer_by_name(layer_name)
        layer.turn(turns)

    def execute(self,moves: str):
        move_array = moves.rstrip().split(' ')
        for move in move_array:
            self.turn(move[0],notation_dict[move[1:]])
    
    def face_to_array(self, face_name: str):
        face = Faces.get_face_by_name(face_name)
        layer = self.get_layer_by_name(face_name)   

        face_array = []

        for holder in layer.piece_holder_array:
            dir_color = holder.piece.dir_color(face.dir)
            face_array.append(Faces.color_to_int[dir_color])
        return face_array

    def cube_to_array(self):
        cube_array=[]

        for face in Faces.face_array:
            cube_array += self.face_to_array(face.name)
        return cube_array

    def display_face(self, face_name: str):
        face = Faces.get_face_by_name(face_name)
        layer = self.get_layer_by_name(face_name)   

        for holder in layer.piece_holder_array:
            print(holder.piece.dir_color(face.dir))

    def solved(self):
        result = True
        for face in Faces.face_array:
            # print(f'checking face {face.name}...')
            layer = self.get_layer_by_name(face.name)
            
            for holder in layer.piece_holder_array:
                # print(f'{holder.piece.dir_color(face.dir)} <-> {face.color}')
                if holder.piece.dir_color(face.dir) != face.color:
                    result = False
                    break

            if result == False:
                break

        return result
    
    def get_state(self):
        
        # state=np.zeros(shape=(3*self.size,4*self.size))
        # cube_array = self.cube_to_array()
        # pf_pos = [[1,2],[0,1],[1,1],[1,0],[2,1],[1,3]]
        # pf_r = [[[1,0,0],[0,1,0]],[[0,-1,self.size-1],[-1,0,self.size-1]],[[0,1,0],[-1,0,self.size-1]],[[1,0,0],[0,-1,self.size-1]],[[0,1,0],[-1,0,self.size-1]],[[0,1,0],[1,0,0]]]

        # cube_array_index=0
        # for face_num in range(Faces.face_count):
        #     for i in range(self.size):
        #         for j in range(self.size):
        #             x=pf_pos[face_num][0]*self.size + i*pf_r[face_num][0][0] + j*pf_r[face_num][0][1] + pf_r[face_num][0][2]
        #             y=pf_pos[face_num][1]*self.size + i*pf_r[face_num][1][0] + j*pf_r[face_num][1][1] + pf_r[face_num][1][2]
        #             state[x][y]=cube_array[cube_array_index]+1
        #             cube_array_index+=1
        state=np.zeros(shape=(self.size,self.size,self.size,Faces.face_count))
        center_offset = (self.size-1)/2
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    piece = self.get_holder_by_pos(Position(x-center_offset,y-center_offset,z-center_offset)).piece
                    # print(piece.color)
                    for face in range(Faces.face_count):
                        dir_color = piece.dir_color(Faces.face_array[face].dir)
                        state[x][y][z][face]=Faces.color_to_int[dir_color]
                        

        return state
    
#%%

if __name__ == "__main__":
    cube_2x2x2 = Cube('3x3x3')
    
    cube_2x2x2.execute("L' U' F L2 F2 D F R2 B2 L' B2 L' U2 F2 B2 D2 B2 R")
    print(cube_2x2x2.cube_to_array())

    print(cube_2x2x2.get_state())
