import openpyxl as xl


class WorksheetDumpControl():


    @staticmethod
    def dump(worksheet, file):
        ws = worksheet

        with open(file, mode='w', encoding='utf8') as f:

            # 各列
            for column_th in range(1, ws.max_column + 1):
                column_letter = xl.utils.get_column_letter(column_th)
                items = []
                items.append(f"width={ws.column_dimensions[column_letter].width}")
                f.write(f"""\
({column_letter}) {' '.join(items)}
""")


            # 各行
            for row_th in range(1, ws.max_row + 1):
                items = []
                items.append(f"height={ws.row_dimensions[row_th].height}")
                f.write(f"""\
({row_th}) {' '.join(items)}
""")


            # 各セル
            for row_th in range(1, ws.max_row + 1):
                for column_th in range(1, ws.max_column + 1):
                    column_letter = xl.utils.get_column_letter(column_th)
                    cell = ws[f'{column_letter}{row_th}']

                    items = []

                    # 背景色を出力
                    sub_items = WorksheetDumpControl.parse_fill(fill=cell.fill)
                    if 0 < len(sub_items):
                        items.append(f"fill=[{' '.join(sub_items)}]")

                    # フォントを出力
                    sub_items = WorksheetDumpControl.parse_font(font=cell.font)
                    if 0 < len(sub_items):
                        items.append(f"font=[{' '.join(sub_items)}]")

                    # 文字寄せを出力
                    sub_items = WorksheetDumpControl.parse_alignment(alignment=cell.alignment)
                    if 0 < len(sub_items):
                        items.append(f"alignment=[{' '.join(sub_items)}]")

                    # 罫線を出力
                    if cell.border is not None:
                        if hasattr(cell.border, 'left') and cell.border.left is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.left)
                            if 0 < len(sub_items):
                                items.append(f"left=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'right') and cell.border.right is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.right)
                            if 0 < len(sub_items):
                                items.append(f"right=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'top') and cell.border.top is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.top)
                            if 0 < len(sub_items):
                                items.append(f"top=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'bottom') and cell.border.bottom is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.bottom)
                            if 0 < len(sub_items):
                                items.append(f"bottom=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'diagonal') and cell.border.diagonal is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.diagonal)
                            if 0 < len(sub_items):
                                items.append(f"diagonal=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'vertical') and cell.border.vertical is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.vertical)
                            if 0 < len(sub_items):
                                items.append(f"vertical=[{' '.join(sub_items)}]")

                        if hasattr(cell.border, 'horizontal') and cell.border.horizontal is not None:
                            sub_items = WorksheetDumpControl.parse_side(side=cell.border.horizontal)
                            if 0 < len(sub_items):
                                items.append(f"horizontal=[{' '.join(sub_items)}]")

                    f.write(f"""\
({column_letter}{row_th}) {' '.join(items)}
""")


    @staticmethod
    def parse_font(font):
        items = []
        if font is not None:
            #name=None, charset=None, family=None, b=False, i=False, strike=None, outline=None, shadow=None, condense=None, color=<openpyxl.styles.colors.Color object>            

            if font.name is not None:
                items.append(f"name={font.name}")

            if font.charset is not None:
                items.append(f"charset={font.charset}")

            if font.family is not None:
                items.append(f"family={font.family}")

            if font.b is not None:
                items.append(f"b={font.b}")

            if font.i is not None:
                items.append(f"i={font.i}")

            if font.strike is not None:
                items.append(f"strike={font.strike}")

            if font.outline is not None:
                items.append(f"outline={font.outline}")

            if font.shadow is not None:
                items.append(f"shadow={font.shadow}")

            if font.condense is not None:
                items.append(f"condense={font.condense}")

            # 色
            sub_items = WorksheetDumpControl.parse_color(color=font.color)
            if 0 < len(sub_items):
                items.append(f"color=[{' '.join(sub_items)}]")

        return items


    @staticmethod
    def parse_fill(fill):
        items = []
        if fill is not None:
            if fill.patternType is not None:
                items.append(f"{fill.patternType}")

            # fg色
            if fill.fgColor is not None:
                sub_items = WorksheetDumpControl.parse_color(color=fill.fgColor)
                if 0 < len(sub_items):
                    items.append(f"fgColor=[{' '.join(sub_items)}]")

        return items


    @staticmethod
    def parse_alignment(alignment):
        items = []
        if alignment is not None:
            if alignment.horizontal is not None:
                items.append(f"horizontal={alignment.horizontal}")

            if alignment.vertical is not None:
                items.append(f"vertical={alignment.vertical}")
        return items


    @staticmethod
    def parse_side(side):
        items = []
        if side.style is not None:
            items.append(f"{side.style}")

        # 色
        sub_items = WorksheetDumpControl.parse_color(color=side.color)
        if 0 < len(sub_items):
            items.append(f"color=[{' '.join(sub_items)}]")

        return items


    @staticmethod
    def parse_color(color):
        items = []
        if color is not None:
            # rgb='00CCCCCC', indexed=None, auto=None, theme=None, tint=0.0, type='rgb'

            if color.type is not None:
                items.append(f"type={color.type}")

                if color.type == 'rgb':
                    if color.rgb is not None:
                        items.append(f"rgb={color.rgb}")

                elif color.type == 'int':
                    if color.indexed is not None:
                        items.append(f"indexed={color.indexed}")

                    if color.theme is not None:
                        items.append(f"theme={color.theme}")

                elif color.type == 'bool':
                    if color.auto is not None:
                        items.append(f"auto={color.auto}")

            if color.tint is not None:
                items.append(f"tint={color.tint}")

        return items
