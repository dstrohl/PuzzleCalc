
from PC.pc_lib import *
from unittest import TestCase


L1 = '0101000000'
M1 = ['0', '1', '.', '.', '.', '.', '.', '.', '.', '.']

L2 = ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0']
M2 = ['0', '0', '.', '.', '1', '1', '.', '.', '.', '.']

L3 = '0000001100'
M3 = '0.....1...'

L4 = '0000000001'
M4 = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1']

L5 = '1010101010'
M5 = '..........'


class TestLineHelper(TestCase):

    def validate_helper(self,
                        item,
                        str_comp=None,
                        bool_comp=None,
                        line_len=None,
                        is_mask=None,
                        is_gt=None,
                        is_lt=None,
                        is_eq=None,
                        is_ne=None,
                        iter_comp=None,
                        ):

        msg = item.dump()
        if str_comp is not None:
            if line_len is None:
                line_len = len(str_comp)
            if is_mask is None:
                is_mask = config.unknown in str_comp
            if bool_comp is None:
                if is_mask:
                    bool_comp = bool(str_comp.replace(config.unknown, ''))
                else:
                    bool_comp = config.filled in str_comp
            if iter_comp is None:
                iter_comp = list(str_comp)

        if str_comp is not None:
            with self.subTest(test_type='str_comp'):
                self.assertEqual(str_comp, str(item), msg=msg)

        if bool_comp is not None:
            with self.subTest(test_type='bool_comp'):
                self.assertEqual(bool_comp, bool(item), msg=msg)

        if line_len is not None:
            with self.subTest(test_type='line_len'):
                self.assertEqual(line_len, len(item), msg=msg)

        if is_mask is not None:
            with self.subTest(test_type='is_mask'):
                self.assertEqual(is_mask, item.is_mask, msg=msg)

        if is_eq is not None:
            if not isinstance(is_eq, (list, tuple)):
                is_eq = [is_eq]
            for i in is_eq:
                with self.subTest(test_type='is_eq', comp=str(i)):
                    self.assertEqual(i, item, msg=msg)

        if is_ne is not None:
            if not isinstance(is_ne, (list, tuple)):
                is_ne = [is_ne]
            for i in is_ne:
                with self.subTest(test_type='is_ne', comp=str(i)):
                    self.assertNotEqual(i, item, msg=msg)

        if is_gt is not None:
            self.assertGreater(10, 1, msg='you messed up the comparison')
            if not isinstance(is_gt, (list, tuple)):
                is_gt = [is_gt]
            for i in is_gt:
                with self.subTest(test_type='is_gt', comp=str(i)):
                    self.assertGreater(item, i, msg=msg)

        if is_lt is not None:
            if not isinstance(is_lt, (list, tuple)):
                is_lt = [is_lt]
            for i in is_lt:
                with self.subTest(test_type='is_lt', comp=str(i)):
                    self.assertLess(item, i, msg=msg)

        if iter_comp is not None:
            with self.subTest(test_type='iter_comp'):
                self.assertEqual(iter_comp, list(item), msg=msg)

    def test_line_init(self):
        self.validate_helper(
            PcLineHelper(L1),
            str_comp=L1,
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=[L3],
            is_lt=[L5],
            is_eq=[L1, M1],
            is_ne=[L2, M2],
            iter_comp=None,
        )

    def test_init_empty_line(self):
        check_eq = PcLineHelper('0000000000')
        self.validate_helper(
            PcLineHelper(line_length=10, is_mask=False),
            str_comp='0000000000',
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=None,
            is_lt=None,
            is_eq=[check_eq, M5],
            is_ne=[L1, M2],
            iter_comp=None,
        )

    def test_init_empty_mask(self):
        self.validate_helper(
            PcLineHelper(line_length=10, is_mask=True),
            str_comp='..........',
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=None,
            is_lt=None,
            is_eq=[M5, L1, L2, L3, L4, L5],
            is_ne=[M2],
            iter_comp=None,
        )

    def test_init_mask_tmp(self):
        tmp_item = PcLineHelper(M2)
        act = tmp_item == M2
        self.assertTrue(act)

    def test_init_mask(self):
        self.validate_helper(
            PcLineHelper(M2),
            str_comp='00..11....',
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=None,
            is_lt=None,
            is_eq=[L2, M2],
            is_ne=[L1, M3],
            iter_comp=None,
        )

    def test_init_force_mask(self):
        self.validate_helper(
            PcLineHelper(L1, is_mask=True),
            str_comp=None,
            bool_comp=None,
            line_len=None,
            is_mask=True,
            is_gt=None,
            is_lt=None,
            is_eq=[L1],
            is_ne=[M1, L2],
            iter_comp=None,
        )

    def test_init_with_list(self):
        self.validate_helper(
            PcLineHelper(L2),
            str_comp='0011110000',
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=None,
            is_lt=None,
            is_eq=[L2, M2, M5],
            is_ne=[L4, M1],
            iter_comp=None,
        )

    def test_init_with_helper(self):
        test_item = PcLineHelper(L3)
        self.validate_helper(
            PcLineHelper(test_item),
            str_comp=L3,
            bool_comp=None,
            line_len=None,
            is_mask=None,
            is_gt=None,
            is_lt=None,
            is_eq=[L3, M3],
            iter_comp=None,
        )

    def test_format(self):
        test_item = PcLineHelper(L1, line_num=1)

        exp_out = '0101000000'
        act_out = test_item.format()
        self.assertEqual(act_out, exp_out)

        # with prefix + wrapped
        exp_out = 'line 1 (10): [0101000000]'
        act_out = test_item.format(prefix='line {line_num} ({line_length}): ', wrapper='[]')
        self.assertEqual(act_out, exp_out)

        # with sep + padding
        exp_out = '| 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |'
        act_out = test_item.format(sep='|', pad_to=3, wrapper='|')
        self.assertEqual(act_out, exp_out)

        # with indent + prefix
        exp_out = '    line foobar: 0101000000'
        act_out = test_item.format(prefix='line {snafu}: ', snafu='foobar', indent_size=4)
        self.assertEqual(act_out, exp_out)

        # with sep
        exp_out = '0,1,0,1,0,0,0,0,0,0'
        act_out = test_item.format(sep=',')
        self.assertEqual(act_out, exp_out)

    def test_set_replace(self):
        test_item = PcLineHelper(L1)
        exp_out = '-+-+------'
        test_item.set_replace(skipped='-', filled='+')
        self.assertEqual(str(test_item), exp_out)

    def test_new_mask(self):
        test_item = PcLineHelper(L1)
        self.assertEqual(test_item, '0101000000')
        self.assertEqual(test_item.is_mask, False)

        test_mask = test_item.new_mask()
        self.assertEqual(test_mask, '..........')
        self.assertEqual(test_mask.is_mask, True)

    def test_make_mask(self):
        i1 = PcLineHelper('0101000000')
        i2 = '0101000011'
        i3 = '0000000000'
        i4 = '1111111111'

        TESTS = [
            # (test_num, [items_in], mask_out),
            (100, [], '0101000000'),
            (101, [i2], '01010000..'),
            (102, [i2, i3], '0.0.0000..'),
            (103, [i2, i4], '.1.1......'),
            (104, [i2, i3, i4], '..........'),
        ]

        for test_num, items_in, mask_out in TESTS:
            with self.subTest(test_num=test_num):
                act_out = i1.make_mask(*items_in)
                self.assertEqual(act_out, mask_out, msg=act_out.dump())

    def test_update(self):
        test_l1 = PcLineHelper(L1)
        test_l3 = PcLineHelper(L3)
        test_l4 = PcLineHelper(L4)
        test_base = PcLineHelper(line_length=10, is_mask=False)
        test_base.update(test_l1, test_l4, test_l3)

        exp_out = '0101001101'
        self.assertEqual(exp_out, test_base)

    def test_get_item(self):
        test_item = PcLineHelper(L1)
        self.assertEqual(test_item[0], '0')
        self.assertEqual(test_item[1], '1')
        self.assertEqual(test_item[2], '0')
        self.assertEqual(test_item[3], '1')
        self.assertEqual(test_item[4], '0')


class TestHelpers(TestCase):

    def test_pc_list(self):
        base = PcList([1, 2, 3])

        TESTS = [
            (0, [99, 2, 3]),
            (1, [1, 99, 3]),
            (2, [1, 2, 99]),
            (3, [1, 2, 3, 99]),
            (4, [1, 2, 3, 0, 99]),
            (5, [1, 2, 3, 0, 0, 99]),
            (6, [1, 2, 3, 0, 0, 0, 99]),
        ]
        for index, exp_out in TESTS:
            new_base = base.copy()
            new_base.set(index, 99, 0)
            self.assertEqual(new_base, exp_out)


    def test_pc_list_pad(self):
        pc_list = PcList()
        self.assertEqual(len(pc_list), 0)

        pc_list.pad(4, 0)
        self.assertEqual(len(pc_list), 4)

        pc_list.pad(2, 0)
        self.assertEqual(len(pc_list), 4)

        pc_list.pad(5, 0)
        self.assertEqual(len(pc_list), 5)

    def test_num_digits(self):
        self.assertEqual(1, num_digits(1))
        self.assertEqual(2, num_digits(10))
        self.assertEqual(3, num_digits(100))

    def test_bool_or_str(self):
        self.assertEqual('test', bol_or_str(True, 'test'))
        self.assertEqual(None, bol_or_str(False, 'test'))
        self.assertEqual('test2', bol_or_str('test2', 'test'))

    def test_split_str(self):
        TESTS = [
            # test one
            (100, '1', [1], True),

            # test 2
            (101, '1, 2', ['1', '2'], False),

            # test 5
            (102, r'1\2\3\4', [1, 2, 3, 4], True),

            # test with extra
            (103, ' 1, 3, 4,,5 ,', [1, 3, 4, 5], True),

            # test with none
            (104, None, [], False),

            # test with strings
            (105, 'x, 0,1,.,0', ['X', '0', '1', '.', '0'], False),
        ]

        for test_num, val_in, exp_out, as_int in TESTS:
            with self.subTest(test_num=test_num):
                act_out = list(split_string(val_in, as_int))
                self.assertEqual(act_out, exp_out)


D0 = {
    'l0': '1,2,3,4',
    'l0m0': 'x',
    'l0m1': '0',
    'l0m2': '.',
    'l0m3': '0',
}

E0 = [
    {
        'mask': ['X', '0', '.', '0'],
        'elements': [1, 2, 3, 4],
    },
]


D1 = {
    'l1': '4',
    'l1m3': 'x',
}

E1 = [
    {
        'mask': ['.', '.', '.', 'X'],
        'elements': [4],
    },
]

D2 = {
    'l2': '5,6,7',
    'l2m0': '0',
    'l2m1': 'x',
    'l2m2': 'x',
    'l2m3': 'x',
}


E2 = [
    {
        'mask': ['0', 'X', 'X', 'X'],
        'elements': [5, 6, 7],
    },
]


class TestConvertList(TestCase):
    def test_1(self):
        dict_in = D0
        exp_out = E0
        act_out = convert_element_dict_to_list(dict_in)
        self.assertEqual(act_out, exp_out)

    def test_2_lines(self):
        dict_in = dict(**D0, **D1)
        exp_out = E0 + E1
        act_out = convert_element_dict_to_list(dict_in)
        self.assertEqual(act_out, exp_out)

    def test_3_lines(self):
        dict_in = dict(**D0, **D1, **D2)
        exp_out = E0 + E1 + E2
        act_out = convert_element_dict_to_list(dict_in)
        self.assertEqual(act_out, exp_out)

    def test_force_line_len(self):
        dict_in = dict(**D0, **D1, **D2)
        exp_out = E0 + E1 + E2
        act_out = convert_element_dict_to_list(dict_in, line_length=10)

        for l in act_out:
            self.assertEqual(len(l['mask']), 10)

    def test_force_row_count(self):
        dict_in = dict(**D0, **D1, **D2)
        exp_out = E0 + E1 + E2
        act_out = convert_element_dict_to_list(dict_in, line_length=10, row_count=10)

        self.assertEqual(len(act_out), 10)
        for l in act_out:
            self.assertEqual(len(l['mask']), 10)


SET_1 = dict(
    test_num=100,
    elements='1',
    mask_in=None,
    mask_out='..........',
    options=[
        '1000000000',
        '0100000000',
        '0010000000',
        '0001000000',
        '0000100000',
        '0000010000',
        '0000001000',
        '0000000100',
        '0000000010',
        '0000000001',
    ],
    error=None,
    replace=None,
)


SET_2 = dict(
    test_num=102,
    elements='5',
    mask_in=None,
    mask_out='..........',
    options=[
        '1111100000',
        '0111110000',
        '0011111000',
        '0001111100',
        '0000111110',
        '0000011111',

    ],
    error=None,
    replace=None,
)

SET_3 = dict(
    test_num=103,
    elements='7',
    mask_in=None,
    mask_out='...1111...',
    options=[
        '1111111000',
        '0111111100',
        '0011111110',
        '0001111111',
    ],
    error=None,
    replace=None,
)
SET_4 = dict(
    test_num=104,
    elements='7,1',
    mask_in=None,
    mask_out='.111111...',
    options=[
        '1111111010',
        '1111111001',
        '0111111101',
    ],
    error=None,
    replace=None,
)
SET_5 = dict(
    test_num=105,
    elements='3/5',
    mask_in=None,
    mask_out='.11..1111.',
    options=[
        '1110111110',
        '1110011111',
        '0111011111',
    ],
    error=None,
    replace=None,
)

SET_6 = dict(
    test_num=106,
    elements='2, 2, 2',
    mask_in=None,
    mask_out='..........',
    options=[
        '1101101100',
        '1101100110',
        '1101100011',
        '1100110110',
        '1100110011',
        '1100011011',
        '0110110110',
        '0110110011',
        '0110011011',
        '0011011011',
    ],
    error=None,
    replace=None,
)

SET_7 = dict(
    test_num=107,
    elements='1,2,5',
    mask_in=None,
    mask_out='1011011111',
    options=['1011011111'],
    error=None,
    replace=None,
)

SET_8 = dict(
    test_num=108,
    elements='1',
    mask_in='000....000',
    mask_out='000....000',
    options=[
        '0001000000',
        '0000100000',
        '0000010000',
        '0000001000',
    ],
    error=None,
    replace=None,
)
SET_9 = dict(
    test_num=109,
    elements='5',
    mask_in='.1.....0.0',
    mask_out='.1111.0000',
    options=[
        '1111100000',
        '0111110000',
    ],
    error=None,
    replace=None,
)

SET_10 = dict(
    test_num=110,
    elements='7',
    mask_in='0........0',
    mask_out='0.111111.0',
    options=[
        '0111111100',
        '0011111110',
    ],
    error=None,
    replace=None,
)

"""
    options=[
        '1111111010',
        '1111111001',
        '0111111101',
    ],
"""

SET_11 = dict(
    test_num=111,
    elements='7,1',
    mask_in='10........',
    mask_out='??????????',
    options=[
    ],
    error=PcException,
    replace=None,
)

SET_12 = dict(
    test_num=112,
    elements='2, 2, 2',
    mask_in='111.......',
    mask_out='??????????',
    options=[],
    error=PcException,
    replace=None,
)


class TestPcLine(TestCase):
    maxDiff = None

    def test_pc_line(self):
        TESTS = [SET_1,
                 SET_2,
                 SET_3,
                 SET_4,
                 SET_5,
                 SET_6,
                 SET_7,
                 SET_8,
                 SET_9,
                 SET_10,
                 SET_11,
                 SET_12,
                 ]

        RUN_TEST = None

        for test in TESTS:
            if RUN_TEST is not None and test['test_num'] != RUN_TEST:
                continue
            with self.subTest(test_num=test['test_num']):
                error = test['error']
                elements = test['elements']
                mask_in = test['mask_in']
                mask_out = PcLineHelper(test['mask_out'], is_mask=True)
                options = []
                for o in test['options']:
                    options.append(list(o))

                replace = test['replace']

                if error is None:
                    pc_line = PcLine(10, elements, knowns=mask_in)
                    msg = '\n\n' + pc_line.dump()
                    with self.subTest(test_type='len'):
                        self.assertEqual(len(options), len(pc_line), msg=msg)
                    with self.subTest(test_type='mask_out_mask'):
                        self.assertEqual(mask_out,  pc_line.line_mask, msg=msg)
                    with self.subTest(test_type='mask_out_func'):
                        self.assertEqual(mask_out,  pc_line.mask(init_col=False), msg=msg)
                    with self.subTest(test_type='data_out'):
                        self.assertEqual(options, pc_line.data(init_col=False), msg=msg)
                    with self.subTest(test_type='title_out'):
                        pass
                    with self.subTest(test_type='header'):
                        exp_header = ['1' ,'2' ,'3' ,'4' ,'5' ,'6' ,'7' ,'8' ,'9' ,'10']
                        self.assertEqual(exp_header, pc_line.header(init_col=False))
                    with self.subTest(test_type='bool'):
                        self.assertTrue(pc_line, msg=msg)
                else:
                    with self.assertRaises(error):
                        PcLine(10, elements, knowns=mask_in, raise_error=True)



'''
class TestPcElementInfo(TestCase):
    maxDiff = None

    def make_elements(self, line_len, *elements):
        return make_info(line_len, *elements)

    def validate_element(self, items, index, length, min_start, max_start, prev_total, next_total):
        with self.subTest(index=index):
            item = items[index]

            if len(items) > 1:
                if index == 0:
                    with self.subTest(test='prev_item'):
                        self.assertIsNone(item.prev_element)
                    with self.subTest(test='next_item'):
                        self.assertIsNotNone(item.next_element)
                if index == len(items) - 1:
                    with self.subTest(test='prev_item'):
                        self.assertIsNotNone(item.prev_element)
                    with self.subTest(test='next_item'):
                        self.assertIsNone(item.next_element)
            else:
                with self.subTest(test='prev_item'):
                    self.assertIsNone(item.prev_element)
                with self.subTest(test='next_item'):
                    self.assertIsNone(item.next_element)

            self.assertEqual(item.index, index)
            with self.subTest(test='length'):
                self.assertEqual(item.length, length)

            with self.subTest(test='min_start'):
                self.assertEqual(item.min_start, min_start)

            with self.subTest(test='max_start'):
                self.assertEqual(item.max_start, max_start)

            with self.subTest(test='prev_total'):
                self.assertEqual(item.prev_total, prev_total)

            with self.subTest(test='next_total'):
                self.assertEqual(item.next_total, next_total)

    def test_init_1(self):
        tmp_el = self.make_elements(5, 3)
        self.validate_element(
            tmp_el,
            index=0,
            length=3,
            min_start=0,
            max_start=2,
            prev_total=4,
            next_total=4,
        )

    def test_init_2(self):
        """
        xxx-xxxxx-
        -xxx-xxxxx
        0123456789
        :return:
        """
        tmp_el = self.make_elements(10, 3, 5)

        self.validate_element(
            tmp_el,
            index=0,
            length=3,
            min_start=0,
            max_start=1,
            prev_total=4,
            next_total=10,
        )

        self.validate_element(
            tmp_el,
            index=1,
            length=5,
            min_start=4,
            max_start=5,
            prev_total=10,
            next_total=6,
        )


    def test_init_3(self):
        """
        xx-xx-xx--
        --xx-xx-xx
        0123456789
        """

        tmp_el = self.make_elements(10, 2, 2, 2)

        self.validate_element(
            tmp_el,
            index=0,
            length=2,
            min_start=0,
            max_start=2,
            prev_total=3,
            next_total=9,
        )

        self.validate_element(
            tmp_el,
            index=1,
            length=2,
            min_start=3,
            max_start=5,
            prev_total=6,
            next_total=6,
        )

        self.validate_element(
            tmp_el,
            index=2,
            length=2,
            min_start=6,
            max_start=8,
            prev_total=9,
            next_total=3,
        )


    def test_init_error(self):
        with self.assertRaises(IndexError):
            tmp_el = self.make_elements(10, 12, 2, 2)

    def test_make_range(self):
        tmp_el = self.make_elements(10, 3, 5)
        TESTS = [
            # (num, index, min_start, exp_range),
            (100, 0, 0, [0, 1]),
            (101, 0, 1, [1]),
            (102, 0, 2, []),
            (103, 0, 3, []),
            (104, 0, 4, []),
            (105, 0, 5, []),
            (106, 0, 6, []),
            (107, 0, 7, []),
            (108, 0, 8, []),
            (109, 0, 9, []),

            (200, 1, 0, [4, 5]),
            (201, 1, 1, [4, 5]),
            (202, 1, 2, [4, 5]),
            (203, 1, 3, [4, 5]),
            (204, 1, 4, [4, 5]),
            (205, 1, 5, [5]),
            (206, 1, 6, []),
            (207, 1, 7, []),
            (208, 1, 8, []),
            (209, 1, 9, []),
        ]
        for t_num, index, min_start, exp_range in TESTS:
            with self.subTest(num=t_num):
                test_item = tmp_el[index]
                act_range = list(test_item.make_range(min_start))
                self.assertEqual(act_range, exp_range)

    def test_make_options_1(self):
        tmp_el = self.make_elements(10, 9)[0]
        act = tmp_el.make_options()
        exp = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '-'],
            ['-', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        ]
        self.assertEqual(act, exp)

        act2 = make_options(10, 9, sep=None, line_sep=None, only_overlap=False)
        self.assertEqual(act2, exp)

    def test_make_options_2(self):
        """
        111-------
        -111------
        --111-----
        ---111----
        ----111---
        -----111--
        ------111-
        -------111

        :return: 
        """
        tmp_el = self.make_elements(10, 3)[0]
        act = tmp_el.make_options()
        exp = [
            ['0', '0', '0', '-', '-', '-', '-', '-', '-', '-', ],
            ['-', '0', '0', '0', '-', '-', '-', '-', '-', '-', ],
            ['-', '-', '0', '0', '0', '-', '-', '-', '-', '-', ],
            ['-', '-', '-', '0', '0', '0', '-', '-', '-', '-', ],
            ['-', '-', '-', '-', '0', '0', '0', '-', '-', '-', ],
            ['-', '-', '-', '-', '-', '0', '0', '0', '-', '-', ],
            ['-', '-', '-', '-', '-', '-', '0', '0', '0', '-', ],
            ['-', '-', '-', '-', '-', '-', '-', '0', '0', '0', ],
        ]
        self.assertEqual(act, exp)

        act2 = make_options(10, 3, sep=None, line_sep=None, only_overlap=False)
        self.assertEqual(act2, exp)


    def test_make_options_3(self):
        """

        '1'-'1'-'1'-'2'-'2'----
        '1'-'1'-'1'--'2'-'2'---
        '1'-'1'-'1'---'2'-'2'--
        '1'-'1'-'1'----'2'-'2'-
        '1'-'1'-'1'-----'2'-'2'
        -'1'-'1'-'1'-'2'-'2'---
        -'1'-'1'-'1'--'2'-'2'--
        -'1'-'1'-'1'---'2'-'2'-
        -'1'-'1'-'1'----'2'-'2'
        --'1'-'1'-'1'-'2'-'2'--
        --'1'-'1'-'1'--'2'-'2'-
        --'1'-'1'-'1'---'2'-'2'
        ---'1'-'1'-'1'-'2'-'2'-
        ---'1'-'1'-'1'--'2'-'2'
        ----'1'-'1'-'1'-'2'-'2'

        :return: 
        """
        tmp_el = self.make_elements(10, 3, 2)[0]
        act = tmp_el.make_options()
        exp = [
            ['0', '0', '0', '-', '1', '1', '-', '-', '-', '-'],
            ['0', '0', '0', '-', '-', '1', '1', '-', '-', '-'],
            ['0', '0', '0', '-', '-', '-', '1', '1', '-', '-'],
            ['0', '0', '0', '-', '-', '-', '-', '1', '1', '-'],
            ['0', '0', '0', '-', '-', '-', '-', '-', '1', '1'],
            ['-', '0', '0', '0', '-', '1', '1', '-', '-', '-'],
            ['-', '0', '0', '0', '-', '-', '1', '1', '-', '-'],
            ['-', '0', '0', '0', '-', '-', '-', '1', '1', '-'],
            ['-', '0', '0', '0', '-', '-', '-', '-', '1', '1'],
            ['-', '-', '0', '0', '0', '-', '1', '1', '-', '-'],
            ['-', '-', '0', '0', '0', '-', '-', '1', '1', '-'],
            ['-', '-', '0', '0', '0', '-', '-', '-', '1', '1'],
            ['-', '-', '-', '0', '0', '0', '-', '1', '1', '-'],
            ['-', '-', '-', '0', '0', '0', '-', '-', '1', '1'],
            ['-', '-', '-', '-', '0', '0', '0', '-', '1', '1'],
        ]
        self.assertEqual(act, exp)
        act2 = make_options(10, 3, 2, sep=None, line_sep=None, only_overlap=False)
        self.assertEqual(act2, exp)

    def test_make_options_4(self):
        """
        '1'-'1'-'2'-'2'-33--
        '1'-'1'-'2'-'2'--33-
        '1'-'1'-'2'-'2'---33
        '1'-'1'--'2'-'2'-33-
        '1'-'1'--'2'-'2'--33
        '1'-'1'---'2'-'2'-33
        -'1'-'1'-'2'-'2'-33-
        -'1'-'1'-'2'-'2'--33
        -'1'-'1'--'2'-'2'-33
        --'1'-'1'-'2'-'2'-33

        :return: 
        """
        tmp_el = self.make_elements(10, 2, 2, 2)[0]
        act = tmp_el.make_options()
        exp = [
            ['0', '0', '-', '1', '1', '-', '2', '2', '-', '-'],
            ['0', '0', '-', '1', '1', '-', '-', '2', '2', '-'],
            ['0', '0', '-', '1', '1', '-', '-', '-', '2', '2'],
            ['0', '0', '-', '-', '1', '1', '-', '2', '2', '-'],
            ['0', '0', '-', '-', '1', '1', '-', '-', '2', '2'],
            ['0', '0', '-', '-', '-', '1', '1', '-', '2', '2'],
            ['-', '0', '0', '-', '1', '1', '-', '2', '2', '-'],
            ['-', '0', '0', '-', '1', '1', '-', '-', '2', '2'],
            ['-', '0', '0', '-', '-', '1', '1', '-', '2', '2'],
            ['-', '-', '0', '0', '-', '1', '1', '-', '2', '2'],
        ]
        self.assertEqual(act, exp)
        act2 = make_options(10, 2, 2, 2, sep=None, line_sep=None, only_overlap=False)
        self.assertEqual(act2, exp)


class TestMakeOptions(TestCase):

    def test_one_line(self):
        act = make_options(10, 9, inc_overlap=False)
        exp = '000000000-\n-000000000'
        self.assertEqual(act, exp)

    def test_only_overlap(self):
        act = make_options(10, 9, inc_data=False)
        exp = '-00000000-'
        self.assertEqual(act, exp)

    def test_only_overlap_2(self):
        act = make_options(10, 3, 3, inc_data=False)
        exp = '----------'
        self.assertEqual(act, exp)

    def test_only_overlap_3(self):
        act = make_options(10, 6, inc_data=False)
        exp = '----00----'
        self.assertEqual(act, exp)

    def test_only_overlap_4(self):
        act = make_options(10, 4, 4, inc_data=False)
        exp = '-000--111-'
        self.assertEqual(act, exp)

    def test_pad_to(self):
        act = make_options(10, 6, pad_to=3, sep='|', inc_data=False)
        exp = ' - | - | - | - | 0 | 0 | - | - | - | - '
        self.assertEqual(act, exp)

    def test_inc_header(self):
        act = make_options(10, 6, pad_to=3, sep='|', inc_header=True, inc_data=False)
        exp = ' 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10\n - | - | - | - | 0 | 0 | - | - | - | - '
        self.assertEqual(act, exp)

'''