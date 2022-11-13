from manim import *
# or: from manimlib import *
from manim_slides import Slide

DEV=False

TITLE_SCALING = 0.7
SUBTITLE_SCALING = 0.5
TEXT_SCALE=0.6
STEP=0.5

class LShapePiece(Polygon):
    def __init__(self, rot=0):
        assert(rot % 90 == 0)
        rot %= 360
        nodes = [
            [-STEP, -STEP, 0],
            [0, -STEP, 0],
            [0, 0, 0],
            [STEP, 0, 0],
            [STEP, STEP, 0],
            [-STEP, STEP, 0]
        ]
        if rot == 0:
            color = '#648FFF'
        elif rot == 90:
            color = '#DC267F'
        elif rot == 180:
            color = '#FE6100'
        elif rot == 270:
            color = '#785EF0'
        
        super().__init__(*nodes, color=color, fill_color=color, fill_opacity=0.5)
        self.rotate(-rot * DEGREES)
        
class Floor(Rectangle):
    def __init__(self, n, **kwargs):
        self.n = n
        super().__init__(width=STEP * n, height = STEP*2, grid_xstep=STEP, grid_ystep=STEP, **kwargs)
        
    def get_coor(self, pos, from_center = True, from_back = False): 
        if from_back:
            pos = self.n - 2 - pos
        ans = self.get_center() if from_center else [0, 0, 0]
        return ans + (pos - self.n * 0.5 + 1) * STEP * RIGHT
    
class InfiniteFloor(VGroup):
    def __init__(self, n, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.org_height = None
        self.n = n
        self.left_floor = Floor(2)
        self.left_floor.move_to(self.get_coor(0))
        self.right_floor = Floor(n - 4)
        self.black_rec = Rectangle(width = STEP * 2 + 0.2, height = STEP * 2 + 0.1, color=BLACK, fill_color=BLACK, fill_opacity=1)
        self.dotdotdot = VGroup(Dot(), Dot(), Dot()).arrange(buff=0.2)
        
        self.add(VGroup(self.left_floor, self.black_rec, self.right_floor).arrange(buff=-0.1))
        self.left_floor.set_z_index(-1)
        self.right_floor.set_z_index(-1)
        
        self.add(self.black_rec)
        self.add(self.left_floor)
        self.add(self.right_floor)
        self.add(self.dotdotdot.move_to(self.black_rec.get_center()))
        
        self.org_height = self.height
        
    def get_coor(self, pos, from_center = True, from_back = False): 
        if from_back:
            pos = self.n - 2 - pos
        ans = self.get_center() if from_center else [0, 0, 0]
        return ans + (pos - self.n * 0.5 + 1) * STEP * RIGHT * self.get_scale()
    
    # this way is very stupid lol
    def get_scale(self):
        if self.org_height is None:
            return 1
        return self.height / self.org_height
    

class HallwayTilingTutorial(Slide):
    def construct(self):
        latex_packages = [
                r"\usepackage[utf8]{inputenc}",
                r"\usepackage[vietnamese]{babel}",
                r"\usepackage{amsmath}",
                ]
        self.texTemplate = TexTemplate(preamble='\n'.join(latex_packages))
        # self.texTemplate.add_to_preamble(r"\usepackage[utf8]{vietnam}")
        
        self.subtitle = None
        # The comment are part number. There are a lot of parts so it would be easier to mark it myself
        self.formulas = MathTex(r"""
        % 1         2    3                4       5       6     7                 8             9     10     11                 12
        {{ cnt_i }} & =  {{ cnt_{i - 1} }} & & +  {{ 4 }} \cdot {{ cnt_{i - 2} }}        & & + {{ 2 }} \cdot {{ cnt_{i - 3} }}  \\
        % 13        14   15                 16     17     18    19                20            21      22    23                24
        {{ sum_i }} & =  {{ sum_{i - 1} }} & & +  {{ 4 }} \cdot {{ sum_{i - 2} }}        & & + {{ 2 }} \cdot {{ sum_{i - 3} }}  \\
        %                                           25    26    27      28    29                 30     31      32   33     34      35
                    &                      & & +  {{ 4 }} \cdot {{ 3 }} \cdot {{ cnt_{i - 2}  }} & & + {{ 2 }} \cdot {{ 6 }} \cdot {{ cnt_{i - 3} }}
        """).set_color_by_tex('cnt', YELLOW).set_color_by_tex('sum', RED).scale(TEXT_SCALE)
        
        self.intro()
        self.problem_statement()
        # ignore this. This was in the original version
        # self.basic_direction()
        self.dp_formula()
        self.dp_optimization()
        
        self.wait()
        
    def intro(self):
        self.title = Text('Hallway Tiling tutorial')
        self.play(Create(self.title))
        self.pause()
        self.play(self.title.animate.to_edge(UP).scale(TITLE_SCALING))
        self.title_underline = Line(LEFT, RIGHT).next_to(self.title, DOWN * 0.5)
        self.title_underline.width = config['frame_width'] - 1
        self.play(Create(self.title_underline, run_time=0.5))
        
    def problem_statement(self):
        self.set_subtitle('Tóm tắt đề bài')
        statement_text = r"Cho một bảng hình chữ nhật có kích thước $2 \times n$ ($n \le 10^{18}$). " \
                r"Có thể xếp một vài miếng ghép hình chữ L vào bảng. " \
                r"Tính tổng độ bao phủ của bảng."
        self.statement = self.tex(statement_text, tex_environment=None).scale(0.7)
        self.statement.next_to(self.subtitle, DOWN)
        self.add(self.statement)
        self.play(FadeIn(self.statement))
        p0 = LShapePiece()
        p90 = LShapePiece(rot=90)
        p180 = LShapePiece(rot=180)
        p270 = LShapePiece(rot=270)
        piece_group = VGroup(p0, p90, p270, p180).arrange()
        piece_group.next_to(self.statement, DOWN)
        self.play(FadeIn(piece_group))
        
        self.pause()
        
        
        # examples
        
        n = 6
        floor = Floor(n)
        x = p0.copy()
        floor.next_to(piece_group, DOWN * 3)
        
        n_text = MathTex(f"n = {n}").next_to(floor, UP * 0.5).scale(TEXT_SCALE)
        
        def make_coverage_text(c):
            return Tex("coverage = ", f"${c}$").next_to(floor, DOWN * 0.5).scale(TEXT_SCALE)
        
        coverage_text = make_coverage_text(0)
        
        self.play(FadeIn(floor), FadeIn(n_text), FadeIn(coverage_text))
        
        # empty
        self.pause()
        
        # example 1
        e1 = p90.copy()
        self.play(
            e1.animate.move_to(floor.get_coor(2)),
            Transform(coverage_text, make_coverage_text(3))
        )
        
        self.pause()
        
        # example 2
        e21 = p0.copy()
        e22 = p270.copy()
        self.play(
            FadeOut(e1),
            e21.animate.move_to(floor.get_coor(0)),
            e22.animate.move_to(floor.get_coor(3)),
            Transform(coverage_text, make_coverage_text(6))
        )
        
        self.pause()
        
        # example 3
        e31 = p0.copy()
        e32 = p90.copy()
        e33 = p180.copy()
        e34 = p270.copy()
        self.play(
            FadeOut(e21),
            FadeOut(e22),
            e34.animate.move_to(floor.get_coor(0)),
            e32.animate.move_to(floor.get_coor(1)),
            e31.animate.move_to(floor.get_coor(3)),
            e33.animate.move_to(floor.get_coor(4)),
            Transform(coverage_text, make_coverage_text(12))
        )
        
        self.pause()
        
        self.clear()
        
    def basic_direction(self):
        self.set_subtitle('Lời giải')
        
        expected_value_text = self.tex("Giá trị kì vọng").scale(TEXT_SCALE)
        
        self.play(Write(expected_value_text))
        self.pause()
        
        count_text = self.tex("Số trường hợp ($cnt$)", color=YELLOW).scale(TEXT_SCALE)
        sum_text = self.tex("Tổng bao phủ\n\ntrong tất cả\n\ntrường hợp ($sum$)", color=RED).scale(TEXT_SCALE)
        
        VGroup(count_text, sum_text).arrange(buff=2)
        self.play(expected_value_text.animate.next_to(self.subtitle, DOWN * 2))
        self.play(
                Transform(expected_value_text.copy(), count_text),
                Transform(expected_value_text.copy(), sum_text)
            )
        self.play(
                FadeIn(Arrow(start=expected_value_text.get_corner(DOWN), end=count_text.get_corner(UP))),
                FadeIn(Arrow(start=expected_value_text.get_corner(DOWN), end=sum_text.get_corner(UP)))
            )
        self.pause()
        
        ans_text = MathTex(r"\text{Đáp án} = \frac{ sum  }{ cnt }", tex_template=self.texTemplate).scale(TEXT_SCALE).shift(DOWN * 2)
        # self.add(index_labels(ans_text[0]))
        ans_text[0][6:9].set_color(RED)
        ans_text[0][10:13].set_color(YELLOW)
            
        # ans_text.set_color_by_text("sum", "red")
        # ans_text.set_color_by_text("cnt", "yellow")
        
        self.play(
                Transform(count_text.copy(), ans_text),
                Transform(sum_text.copy(), ans_text)
        )
        self.play(
                FadeIn(Arrow(start=count_text.get_corner(DOWN), end=ans_text.get_corner(UP))),
                FadeIn(Arrow(start=sum_text.get_corner(DOWN), end=ans_text.get_corner(UP)))
            )
        
        self.pause()
        
        self.clear()
        
    def dp_formula(self):
        self.set_subtitle('Lời giải: công thức quy hoạch động')
        
        definition_text = r"""
        Gọi {{ $cnt_i$ }} là số lượng cách xếp cho hình chữ nhật kích thước $2 \times i$
        
        Gọi {{ $sum_i$ }} là tổng bao phủ trong tất cả các cách xếp hình chữ nhật kích thước $2 \times i$
        """
        
        definition = self.tex(definition_text, tex_environment=None).next_to(self.subtitle, DOWN, buff=0.1).scale(TEXT_SCALE)
        definition.set_color_by_tex('cnt', YELLOW)
        definition.set_color_by_tex('sum', RED)
        
        self.play(FadeIn(definition))
        self.pause()
        
        class FloorGroup(VGroup):
            def __init__(self, sub, pieces=[]):
                self.n = 8
                self.sub = sub
                self.inf_floor = InfiniteFloor(self.n)
                self.n_text = MathTex("n").next_to(self.inf_floor, UP).scale(TEXT_SCALE)
                self.up_brace = Brace(self.inf_floor, UP)
                
                self.n_sub_text = MathTex(f"n - {sub}").scale(TEXT_SCALE)
                p1 = self.inf_floor.get_coor(-1)
                p2 = self.inf_floor.get_coor(self.n - 1 - sub)
                self.down_brace = BraceBetweenPoints(p1, p2)
                self.n_sub_text.next_to(self.down_brace, DOWN)
                objs = [self.n_text, self.up_brace, self.inf_floor, self.down_brace, self.n_sub_text]
                
                super().__init__(*objs)
                self.arrange(DOWN, coor_mask=[0, 1, 0], buff=0.1)
                
                self.filling_area = Rectangle(
                        width=STEP * sub,
                        height=STEP * 2,
                        color=YELLOW,
                        fill_color=YELLOW,
                        fill_opacity=0.2
                ).move_to(self.inf_floor.get_coor(-1 + sub * 0.5, from_back=True))
                
                self.add(self.filling_area)
                
                for piece in pieces:
                    self.add(piece[0].move_to(self.inf_floor.get_coor(piece[1], from_back=True)))
                self.scale(0.5)
                
        formulas = self.formulas
            
        formulas.next_to(definition, DOWN)
        
        self.play(Write(formulas[1:3]), Write(formulas[13:15]))
        
        
        g1 = FloorGroup(1).next_to(formulas, DOWN)
        self.play(FadeIn(g1))
        self.wait()
        self.pause()
        
        self.play(Transform(g1.n_sub_text.copy(), formulas[3]))
        self.pause()
        self.play(Transform(g1.n_sub_text.copy(), formulas[15]))
        self.pause()
        
        self.play(Transform(g1, FloorGroup(2).move_to(g1.get_center())))
        self.pause()
        
        g2 = [FloorGroup(2) for i in range(4)]
        g2g = VGroup(*g2).arrange_in_grid(row=2, col=2).next_to(formulas, DOWN)
        self.play(Transform(g1, g2[0]))
        g1copy = [g1.copy() for i in range(4)]
        self.play( *(Transform(g1copy[i], g2[i]) for i in range(1, 4)))
        
        pieces = []
        for i in range(4):
            piece = LShapePiece(i * 90).scale(0.5)
            piece.move_to(g2[i].inf_floor.get_coor(0, from_back=True))
            pieces.append(piece)
        
        self.play(FadeIn(*pieces))
        self.pause()
        
        n_sub_texts = [i.n_sub_text for i in g2]
        self.play(Write(formulas[4:7]), *(Transform(i.copy(), formulas[7]) for i in n_sub_texts))
        self.wait()
        self.pause()
        
        self.play(Write(formulas[16:19]), *(Transform(i.copy(), formulas[19]) for i in n_sub_texts))
        self.wait()
        self.pause()
        
        self.play(
            Write(formulas[24:27]), 
            *(Transform(i.copy(), formulas[27:28]) for i in pieces)
        )
                  
        self.wait();
        self.pause()
        
        self.play(
            *(Transform(i.copy(), formulas[28:30]) for i in n_sub_texts)
        )
        self.wait()
        self.pause()
        
        self.play(FadeOut(*pieces, *g1copy[1:4]))
        self.play(g1.animate.next_to(formulas, DOWN))
        self.pause()
        
        self.play(Transform(g1, FloorGroup(3).next_to(formulas, DOWN)))
        self.pause()
        
        g3 = VGroup(g1.copy(), g1.copy()).arrange(LEFT).next_to(formulas, DOWN)
        
        g1copy = g1.copy()
        
        self.play(
            g1.animate.move_to(g3[0]),
            g1copy.animate.move_to(g3[1])
        )
        
        self.pause()
        
        pieces = [
            LShapePiece(0).move_to(g1.inf_floor.get_coor(1, from_back=True)), LShapePiece(180).move_to(g1.inf_floor.get_coor(0, from_back=True)),
            LShapePiece(270).move_to(g1copy.inf_floor.get_coor(1, from_back=True)), LShapePiece(90).move_to(g1copy.inf_floor.get_coor(0, from_back=True))
        ]
        
        for piece in pieces:
            piece.scale(0.5)
        
        self.play(FadeIn(*pieces))
        self.pause()
        
        n_sub_texts = [g1.n_sub_text, g1copy.n_sub_text]
        self.play(Write(formulas[8:11]), *(Transform(i.copy(), formulas[11]) for i in n_sub_texts))
        self.wait()
        self.pause()
        
        self.play(Write(formulas[20:23]), *(Transform(i.copy(), formulas[23]) for i in n_sub_texts))
        self.wait()
        self.pause()
        
        self.play(
            Write(formulas[30:32]), 
            *(Transform(i.copy(), formulas[32:34]) for i in pieces)
        )
                  
        self.wait();
        self.pause()
        
        self.play(
                *(Transform(i.copy(), formulas[34:36]) for i in n_sub_texts)
        )
        self.wait()
        self.pause()
        
        complexity_text = self.tex(r"""
            Công thức trên cho ta lời giải $O(n)$.
        """).scale(TEXT_SCALE).next_to(g3, DOWN)
        
        self.play(Write(complexity_text))
        self.pause()
        
        self.add(self.formulas)
        self.clear(self.formulas)
        
    def dp_optimization(self):
        self.set_subtitle('Lời giải: tối ưu hóa quy hoạch động')
        
        self.play(self.formulas.animate.next_to(self.subtitle, DOWN))
        
        self.pause()
        
        matrix_text = np.array([
                ("~"            , "cnt_{i - 1}" , "cnt_{i - 2}" , "cnt_{i - 3}" , "sum_{i - 1}" , "sum_{i - 2}" , "sum_{i - 3}" ),
                ("cnt_i"        , "1"           , "4"           , "2"           , "0"           , "0"           , "0"           ),
                ("cnt_{i - 1}"  , "1"           , "0"           , "0"           , "0"           , "0"           , "0"           ),
                ("cnt_{i - 2}"  , "0"           , "1"           , "0"           , "0"           , "0"           , "0"           ),
                ("sum_i"        , "0"           , "4 \cdot 3"   , "2 \cdot 6"   , "1"           , "4"           , "2"           ),
                ("sum_{i - 1}"  , "0"           , "0"           , "0"           , "1"           , "0"           , "0"           ),
                ("sum_{i - 2}"  , "0"           , "0"           , "0"           , "0"           , "1"           , "0"           )
                ])
        
        data_matrix = Matrix(matrix_text[1:,1:], h_buff=2, bracket_h_buff=1, element_alignment_corner=DOWN).scale(TEXT_SCALE)
        matrix_row_labels = []
        matrix_col_labels = []
        data_matrix_entries = data_matrix.get_entries()
        row_cnt = len(matrix_text) - 1
        for i in range(1, len(matrix_text)):
            row_label = self.set_tex_color(MathTex(matrix_text[i, 0])).scale(TEXT_SCALE)
            col_label = self.set_tex_color(MathTex(matrix_text[0, i])).scale(TEXT_SCALE)
            col_label.next_to(data_matrix_entries[i - 1], UP)
            row_label.next_to(data_matrix_entries[(i - 1) * row_cnt], LEFT, buff=1.6)
            matrix_col_labels.append(col_label)
            matrix_row_labels.append(row_label)
            
        matrix_group = VGroup(data_matrix, *matrix_row_labels, *matrix_col_labels).next_to(self.formulas, DOWN, buff=1)
        
        self.play(
            *[Write(cell) for cell in matrix_row_labels + matrix_col_labels],
            *[Create(bracket) for bracket in data_matrix.get_brackets()]
        )
        
        self.pause()
        
        sr = SurroundingRectangle(data_matrix.get_rows()[0])
        
        self.play(Write(sr))
        self.pause()
                
        self.play(
            Transform(self.formulas[3].copy(), data_matrix_entries[0]),
            Transform(self.formulas[5].copy(), data_matrix_entries[1]),
            Transform(self.formulas[9].copy(), data_matrix_entries[2])
        )
        self.pause()
        
        sr2 = SurroundingRectangle(data_matrix.get_rows()[3])
        self.play(Unwrite(sr), Write(sr2))
        self.pause()
        
        self.play(
            Transform(self.formulas[15].copy(), data_matrix_entries[3 * row_cnt + 3]),
            Transform(self.formulas[17].copy(), data_matrix_entries[3 * row_cnt + 4]),
            Transform(self.formulas[21].copy(), data_matrix_entries[3 * row_cnt + 5])
        )
        self.pause()
        self.play(
            Transform(self.formulas[25:28].copy(), data_matrix_entries[3 * row_cnt + 1]),
            Transform(self.formulas[31:34].copy(), data_matrix_entries[3 * row_cnt + 2])
        )
        self.pause()
        
        self.play(Unwrite(sr2))
        
        self.pause()
        
        zeros = []
        ones = []
        for i in range(row_cnt):
            for f in range(row_cnt):
                if matrix_text[i + 1][f + 1] == '1':
                    ones.append(data_matrix_entries[i * row_cnt + f])
                if matrix_text[i + 1][f + 1] == '0':
                    zeros.append(data_matrix_entries[i * row_cnt + f])
        
        self.play(*[FadeIn(i) for i in ones])
        self.pause()
        self.play(*[FadeIn(i) for i in zeros])
        self.pause()
        
        self.add(matrix_group)
        
        self.clear(matrix_group)
        
        self.play(matrix_group.animate.move_to(ORIGIN))
        self.pause()
        
        equal = MathTex("=").scale(TEXT_SCALE)
        cross = MathTex(r"\times").scale(TEXT_SCALE)
        
        res_matrix = Matrix(matrix_text[1:,0:1], element_alignment_corner=DOWN).scale(TEXT_SCALE)
        base_matrix = Matrix(matrix_text[0:1,1:].reshape(row_cnt, 1), element_alignment_corner=DOWN).scale(TEXT_SCALE)
        
        for i in [*res_matrix.get_entries(), *base_matrix.get_entries()]:
            self.set_tex_color(i)
        
        data_matrix_cpy = data_matrix.copy()
        matrix_group2 = VGroup(res_matrix, equal, data_matrix_cpy, cross, base_matrix).arrange().next_to(self.subtitle, DOWN)
        
        self.play(
            *[Transform(u, v) for u, v in zip(matrix_row_labels, res_matrix.get_entries())],
            *[Transform(u, v) for u, v in zip(matrix_col_labels, base_matrix.get_entries())],
            *[Transform(data_matrix, data_matrix_cpy)],
            *[FadeIn(bracket ) for bracket in res_matrix.get_brackets() + base_matrix.get_brackets()],
            FadeIn(equal),
            FadeIn(cross)
        )
        self.pause()
        self.remove(*matrix_row_labels)
        self.remove(*matrix_col_labels)
        self.add(res_matrix)
        self.add(base_matrix)
                
        res_matrix2 = Matrix(np.array([['cnt_n', 'cnt_{n - 1}', 'cnt_{n - 2}', 'sum_n', 'sum_{n - 1}', 'sum_{n - 2}']]).reshape(row_cnt, 1), element_alignment_corner=DOWN).scale(TEXT_SCALE).move_to(res_matrix.get_center())
        base_matrix2 = Matrix(np.array([['cnt_0', 'cnt_{- 1}', 'cnt_{- 2}', 'sum_0', 'sum_{- 1}', 'sum_{- 2}']]).reshape(row_cnt, 1), element_alignment_corner=DOWN).scale(TEXT_SCALE).move_to(base_matrix.get_center())
        
        for i in [*res_matrix2.get_entries(), *base_matrix2.get_entries()]:
            self.set_tex_color(i)
            
        power = MathTex('n').scale(TEXT_SCALE)
        power.next_to(data_matrix.get_corner(UR), RIGHT)
        data_matrix_cpy = data_matrix.copy()
        equal_cpy = equal.copy()
        cross_cpy = cross.copy()
        matrix_group3 = VGroup(res_matrix2, equal_cpy, data_matrix_cpy, power, cross_cpy, base_matrix2).arrange(coor_mask=[1, 0, 0]).next_to(self.subtitle, DOWN)
        self.play(
            Transform(res_matrix, res_matrix2),
            Transform(base_matrix, base_matrix2),
            Transform(equal, equal_cpy),
            Transform(cross, cross_cpy),
            Transform(data_matrix, data_matrix_cpy),
            FadeIn(power)
        )
        self.pause()
        
        with_text = self.tex('với').scale(TEXT_SCALE)
        base_value_matrix = Matrix(np.array([1, 0, 0, 0, 0, 0]).reshape(row_cnt, 1)).scale(TEXT_SCALE * 0.7)
        base_matrix2_cpy = base_matrix2.copy().scale(0.7)
        
        equal_cpy2 = equal.copy()
        value_group = VGroup(with_text, base_matrix2_cpy, equal_cpy2, base_value_matrix).arrange().next_to(matrix_group3, DOWN)
        
        self.play(
            Transform(base_matrix2.copy(), base_matrix2_cpy),
            FadeIn(with_text),
            FadeIn(equal_cpy2),
            FadeIn(base_value_matrix)
        )
        self.pause()
        self.add(matrix_group3)
        self.clear(matrix_group3)
        
        complexity_text = self.tex(r"""
        Tối ưu này cho ta lời giải $O(6^3 \log n) = O(\log n)$
        """).scale(TEXT_SCALE).next_to(matrix_group3, DOWN, buff=1)
        self.play(Write(complexity_text))
        self.pause()
        
        self.clear()
        
        
    def set_tex_color(self, tex_obj):
        return tex_obj.set_color_by_tex('cnt', YELLOW).set_color_by_tex('sum', RED)
        
    def tex(self, *args, **kwargs):
        return Tex(*args, tex_template=self.texTemplate, **kwargs)
        
    def set_subtitle(self, subtitle):
        old_subtitle = self.subtitle
        self.subtitle = Text(subtitle, color='yellow').next_to(self.title, 0.5 * DOWN).scale(SUBTITLE_SCALING)
        if old_subtitle is not None:
            self.play(Transform(old_subtitle, self.subtitle), run_time=0.5)
            self.remove(old_subtitle)
            self.add(self.subtitle)
        else:
            self.play(Write(self.subtitle), run_time=0.5)
    
    def clear(self, *args):
        exclusion = set([self.title, self.subtitle, self.title_underline] + list(args))
        def is_removable(x):
            return x not in exclusion
        
        removables = [obj for obj in self.mobjects if is_removable(obj)]
        self.play(*[FadeOut(obj) for obj in removables])
        for obj in removables:
            self.remove(obj)
            
    def play(self, *args, **kwargs):
        if DEV:
            self.dev_play(*args, **kwargs)
        else:
            super().play(*args, **kwargs)
        
    def dev_play(self, *args, run_time=None, **kwargs):
        RUN_TIME_SCALE = 0.2
        if DEV:
            if run_time is None:
                run_time = RUN_TIME_SCALE
            else:
                run_time *= RUN_TIME_SCALE
        
        super().play(*args, run_time=run_time, **kwargs)
            
