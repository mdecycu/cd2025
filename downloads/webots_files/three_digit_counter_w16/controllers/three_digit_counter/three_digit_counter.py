from controller import Supervisor

class SevenSegmentController:
    def __init__(self, supervisor, color_on, color_off):
        self.supervisor = supervisor

        # 各位數的 segment material DEF 名稱
        self.segment_material_defs = [
            ["a1mat", "b1mat", "c1mat", "d1mat", "e1mat", "f1mat", "g1mat"],  # 個位數
            ["a2mat", "b2mat", "c2mat", "d2mat", "e2mat", "f2mat", "g2mat"],  # 十位數
            ["a3mat", "b3mat", "c3mat", "d3mat", "e3mat", "f3mat", "g3mat"]   # 百位數
        ]

        # 0-9 的七段顯示樣式 (a,b,c,d,e,f,g)
        self.segment_patterns = [
            [1,1,1,1,1,1,0],  # 0
            [0,1,1,0,0,0,0],  # 1
            [1,1,0,1,1,0,1],  # 2
            [1,1,1,1,0,0,1],  # 3
            [0,1,1,0,0,1,1],  # 4
            [1,0,1,1,0,1,1],  # 5
            [1,0,1,1,1,1,1],  # 6
            [1,1,1,0,0,0,0],  # 7
            [1,1,1,1,1,1,1],  # 8
            [1,1,1,1,0,1,1],  # 9
        ]

        self.color_on = color_on
        self.color_off = color_off

        self.segment_fields = []
        for digit in self.segment_material_defs:
            digit_fields = []
            for mat_def in digit:
                mat_node = supervisor.getFromDef(mat_def)
                if mat_node is None:
                    raise RuntimeError(f"DEF {mat_def} not found in scene tree.")
                color_field = mat_node.getField("diffuseColor")
                digit_fields.append(color_field)
            self.segment_fields.append(digit_fields)

    def set_digit(self, digit_index, value):
        """digit_index: 0=個位, 1=十位, 2=百位; value: 0~9"""
        pattern = self.segment_patterns[value]
        for i, seg_on in enumerate(pattern):
            color = self.color_on if seg_on else self.color_off
            self.segment_fields[digit_index][i].setSFColor(color)

    def display_number(self, number):
        """顯示 0~999 的整數"""
        if not (0 <= number <= 999):
            print("Value out of range (0-999)")
            return
        hundreds = number // 100
        tens = (number % 100) // 10
        units = number % 10
        self.set_digit(2, hundreds)
        self.set_digit(1, tens)
        self.set_digit(0, units)

if __name__ == "__main__":
    supervisor = Supervisor()
    color_on = [0.0, 1.0, 0.0]   # 亮時的顏色
    color_off = [0.0, 0.0, 0.0]  # 滅時的顏色
    display = SevenSegmentController(supervisor, color_on, color_off)

    timestep = int(supervisor.getBasicTimeStep())
    number = 789  # 可以修改這行來顯示不同數字

    while supervisor.step(timestep) != -1:
        display.display_number(number)