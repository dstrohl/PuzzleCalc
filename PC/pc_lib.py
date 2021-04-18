from collections import namedtuple, UserList
from copy import deepcopy

__all__ = ['PcElementInfo', 'PcLine', 'bol_or_str', 'split_string', 'config', 'PcException',
           'PcMatrix', 'num_digits', 'PcLineHelper', 'PcList']

"""

urls

http://<server>:<port>/pc/calc?length=10&size=3,2,3


alternatives:

1 element:
    111-------
    -111------
    --111-----
    ---111----
    ----111---
    -----111--
    ------111-
    -------111

2 elements  
    111-22----
    111--22---
    111---22--
    111----22-
    111-----22
    -111-22---
    -111--22--
    -111---22-
    -111----22
    --111-22--
    --111--22-
    --111---22
    ---111-22-
    ---111--22
    ----111-22


3 elements, 10 spots:
    11-22-33--
    11-22--33-
    11-22---33
    11--22-33-
    11--22--33
    11---22-33
    -11-22-33-
    -11-22--33
    -11--22-33
    --11-22-33



3 elements, 12 spots:
    11-22-33----
    11-22--33---
    11-22---33--
    11-22----33-
    11-22-----33
    11--22-33---
    11--22--33--
    11--22---33-
    11--22----33
    11---22-33--
    11---22--33-
    11---22---33
    11----22-33-
    11----22--33
    11-----22-33
    -11-22-33---
    -11-22--33--
    -11-22---33-
    -11-22----33
    -11--22-33--
    -11--22--33-
    -11--22---33
    -11---22-33-
    -11---22--33
    -11----22-33
    --11-22-33--
    --11-22--33-
    --11-22---33
    --11--22-33-
    --11--22--33
    ---11-22-33-
    ---11-22--33
    ---11--22-33
    ----11-22-33


    ...


output strings = 
    - = unknown
    X = skipped cell
    0 = filled cell

"""

"""
elements add up to more than line length
invalid character in element list
invalid character in mask
no option matches mask
mask too long for line length
"""

class PcList(UserList):
    """
    inserts lists items:
    [1,2].set(4,3,0)
    [1,2,0,0,4]

    """
    def set(self, index, item, default):
        self.pad(index + 1, default)
        self[index] = item

    def pad(self, length, default):
        while len(self) < length:
            self.append(deepcopy(default))


class PcException(Exception):
    pass


class PcConfig(object):
    unknown = '.'
    skipped = '0'
    filled = '1'
    error = '?'
    split_on = r',/\| #*'


config = PcConfig()


def num_digits(int_in):
    return len(str(int(int_in)))


'''
def compare_items(item_one, *items_in):
    tmp_ret = item_one
    for i in items_in:
        if tmp_ret == OC.unknown:
            tmp_ret = i
        else:
            if i == OC.unknown or i == tmp_ret:
                continue
            return OC.unknown
    return tmp_ret


def mask_lists(*data_in):
    """
    compares two or more lists and returns the items that are the same
    """
    tmp_ret = [OC.unknown] * len(data_in[0])
    for index, item in enumerate(zip(*data_in)):
        tmp_ret[index] = compare_items(*item)
    return tmp_ret


def merge_list(*data_in):
    """
    compares two or more lists and merges them together.
    """
    tmp_ret = [OC.skipped] * len(data_in[0])
    for item in data_in:
        for index, c in item:
            if c == OC.filled:
                tmp_ret[index] = c
    return tmp_ret


def filter_lists(mask_in, *data_in):
    """
    goes through a list of lists and removes ones that do not match a filter mask.
    """
    tmp_ret = []

    for row in data_in:
        skip = False
        for i, c in enumerate(row):
            if mask_in[i] != OC.unknown and c != mask_in[i]:
                skip = True
                break
        if not skip:
            tmp_ret.append(row)
    return tmp_ret

'''


def bol_or_str(val_in, default_str):
    if isinstance(val_in, bool):
        if val_in:
            return default_str
        else:
            return None
    return val_in


'''
def replace_values(data_in, alt_values=None):
    if alt_values is None:
        return data_in
    tmp_ret = []
    for c in data_in:
        tmp_ret.append(alt_values.get(c, c))
    return tmp_ret
'''
'''
def vert_nums(start, end, as_string=False, line_sep='\n', pad_with=None, sep=''):
    """
    :param start: what number to start with
    :param end: what number to end with
    :param as_string: return as a string instead of a list
    :param line_sep: use as a line sep
    :param pad_with: if not None, lines will be left padded with this string.
    :param sep: used to seperate each item in a string return.
    :return:
        from 100-102

        as_string:
            with sep ('|'):
                1|1|1\n0|0|0\n0|1|2
            else
                111\n000\n012

        otherwise:
            with sep ('\n')
                ['1\n0\n0',1\n0\n1','1\n\n2']
            else:
                [['1', '1', '1'], ['0', '0', '0'],['0', '1', '2']]
    """
    tmp_rng = list(range(start, end + 1))
    max_digits = num_digits(tmp_rng[-1])
    tmp_rng = map(str, tmp_rng)

    if as_string:
        if max_digits == 1:
            return sep.join(tmp_rng)
        lines = []
        for i in range(max_digits):
            lines.append([])
        for item in tmp_rng:
            if pad_with:
                item = item.rjust(max_digits, pad_with)
            for index in range(max_digits):
                lines[index].append(item[index])
        tmp_ret = []
        for l in lines:
            tmp_ret.append(sep.join(l))
        return line_sep.join(tmp_ret)

    else:
        if sep is not None:
            if max_digits == 1:
                return sep.join(tmp_rng)
            tmp_ret = []
            for item in tmp_rng:
                if pad_with:
                    item = item.rjust(max_digits, pad_with)
                item = line_sep.join(item.split())
                tmp_ret.append(item)
            return tmp_ret
        else:
            if max_digits == 1:
                return tmp_rng
            tmp_ret = []
            for item in tmp_rng:
                if pad_with:
                    item = item.rjust(max_digits, pad_with)
                item = line_sep.join(item.split())
                tmp_ret.append(item)
            return tmp_ret
'''


def split_string(item_in, as_int=True, check_dot=False):
    if isinstance(item_in, (list, tuple, map)):
        if as_int:
            item_in = map(int, item_in)
        return list(item_in)

    if item_in is None:
        return []

    if not isinstance(item_in, str):
        raise TypeError('%r is not a string, list, or tuple' % item_in)

    item_in = item_in.upper().strip(config.split_on)

    check_split = config.split_on
    if check_dot:
        check_split += '.'

    for s in check_split:
        if s in item_in:
            item_in = item_in.split(s)
            break

    if isinstance(item_in, str):
        item_in = list(item_in)

    item_in = map(str.strip, item_in)
    item_in = filter(None, item_in)
    if as_int:
        item_in = map(int, item_in)
    return list(item_in)



'''
def short_format_element_list(list_in, indent_size=0, empty_string='No Items', number_lines=True):
    indent_str = ' ' * indent_size
    if not list_in:
        return indent_str + empty_string
    if not isinstance(list_in[0], list):
        list_in = [list_in]

    tmp_ret = []
    for index, l in enumerate(list_in):
        line_prefix = indent_str
        if number_lines:
            line_prefix += 'Line: ' + str(index + 1).rjust(3, '0') + ' | '
        tmp_ret.append(line_prefix + ''.join(l))

    tmp_ret = '\n'.join(tmp_ret)
    return tmp_ret
'''


class PcLineHelper(object):
    is_mask = None
    line_length = None

    def __init__(self, items=None, replace_values_with=None, is_mask=None, line_length=None, **kwargs):
        self.replace_values = replace_values_with
        self.kwargs = kwargs

        if items is None and is_mask is None:
            raise TypeError('is_mask must be passed if no items are passed.')
        if items is None and line_length is None:
            raise TypeError('line_length must be passed if no items are passed.')

        if is_mask is None:
            if isinstance(items, PcLineHelper):
                is_mask = items.is_mask
            else:
                is_mask = config.unknown in items
        self.is_mask = is_mask

        if line_length is None:
            line_length = len(items)

        if is_mask:
            self.items = [config.unknown] * line_length
        else:
            self.items = [config.skipped] * line_length
        self.line_length = len(self.items)

        if items:
            if len(items) > self.line_length:
                raise IndexError(
                    'Items list %r is longer than the expected number of items: %s' % (items, self.line_length))
            if isinstance(items, str):
                items = split_string(items, as_int=False)
            elif isinstance(items, PcLineHelper):
                self.replace_values = items.replace_values
                items = items.items
            else:
                items = list(map(str.strip, map(str, items)))
            for i, c in enumerate(items):
                try:
                    self[i] = c
                except IndexError:
                    raise IndexError('List assignment index %s our of range for %r' % (i, self.items))

    def dump(self):
        tmp_ret = f'LineHelper("{self}", is_mask={self.is_mask})'
        return tmp_ret

    def format(self, prefix=None, sep='', indent_size=0, pad_to=0, wrapper=None, **kwargs):
        if pad_to:
            tmp_items = []
            for i in self:
                tmp_items.append(i.center(pad_to, ' '))
        else:
            tmp_items = self.items

        if self.replace_values:
            for i, c in enumerate(tmp_items):
                tmp_items[i] = self.replace_values.get(c, c)

        tmp_ret = sep.join(tmp_items)
        if wrapper:
            if len(wrapper) == 1:
                tmp_ret = wrapper + tmp_ret + wrapper
            else:
                tmp_ret = wrapper[0] + tmp_ret + wrapper[1]
        if prefix:
            if '{' in prefix:
                tmp_kwargs = self.kwargs.copy()
                tmp_kwargs.update(kwargs)
                prefix = prefix.format(
                    line_length=self.line_length,
                    **tmp_kwargs
                )
            tmp_ret = prefix + tmp_ret

        if indent_size:
            indent_str = ' ' * indent_size
            tmp_ret = indent_str + tmp_ret

        return tmp_ret

    def set_replace(self, replace_items=None, unknown=None, skipped=None, filled=None):
        tmp_item = replace_items or {}
        if unknown is not None:
            tmp_item[config.unknown] = unknown
        if skipped is not None:
            tmp_item[config.skipped] = skipped
        if filled is not None:
            tmp_item[config.filled] = filled
        self.replace_values = tmp_item

    def make_mask(self, *others):
        """
        pch.make_mask(*pch) returns a mask of item and all passed items
        :param others:
        :return: mask object.
        """

        others = list(others)
        for i, o in enumerate(others):
            others[i] = self.__class__(o)
        others.insert(0, self)

        tmp_ret = self.new_mask()

        for index, item in enumerate(zip(*others)):
            tmp_item = config.unknown
            for i in item:
                if tmp_item == config.unknown:
                    tmp_item = i
                else:
                    if i == config.unknown or i == tmp_item:
                        continue
                    tmp_item = config.unknown
                    break
            tmp_ret[index] = tmp_item
        return tmp_ret

    def new_mask(self):
        tmp_mask = [config.unknown] * self.line_length
        tmp_ret = self.__class__(tmp_mask, replace_values_with=self.replace_values, is_mask=True)
        return tmp_ret

    def update(self, *others):
        """
        pch.add(pch)
        adds any selected items in others to the items in this one, replacing any existing items.
        only works with line items, not masks.
        """
        if self.is_mask:
            raise TypeError('Cannot add items to a mask')

        for item in others:
            item = PcLineHelper(item)
            if item.is_mask:
                raise TypeError('Cannot add mask items to a line item')
            for i, c in enumerate(item):
                if c == config.filled:
                    self[i] = c

    def filter(self, other):
        return self == other

    def __str__(self):
        return self.format()

    def __repr__(self):
        return self.dump()

    def __iter__(self):
        for i in self.items:
            yield i

    def __getitem__(self, item):
        return self.items[item]

    def __setitem__(self, key, value):
        self.items[key] = value

    def __compare__(self, other):
        other = self.__class__(other)
        if other.line_length != self.line_length:
            raise TypeError('Cannot compare different sized lines: self: %r and other: %r' % (self, other))
        if other.is_mask != self.is_mask:
            raise TypeError('cannot compare a line with a mask unless using "==" or "!="')

        other = str(other)
        me = str(self)

        if me == other:
            return 0
        if me > other:
            return 1
        if me < other:
            return -1
        return 0

    def __eq__(self, other):
        other = self.__class__(other)

        if other.line_length != self.line_length:
            raise TypeError('Cannot compare different sized lines (self: %r and other: %r' % (self, other))

        if other.is_mask != self.is_mask:
            if other.is_mask:
                line = self
                mask = other
            else:
                line = other
                mask = self
            for l, m in zip(line, mask):
                if m == config.unknown:
                    continue
                if l != m:
                    return False
            return True
        else:
            return self.__compare__(other) == 0

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self.__compare__(other) >= 0

    def __gt__(self, other):
        return self.__compare__(other) > 0

    def __le__(self, other):
        return self.__compare__(other) <= 0

    def __lt__(self, other):
        return self.__compare__(other) < 0

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return self.line_length

    def __bool__(self):
        """
        if mask:
            bool(pch)  returns if any mask items
        else:
            bool(pch)  returns if any selected
        """
        if self.is_mask:
            tmp_items = str(self)
            tmp_items = tmp_items.replace(config.unknown, '')
            return bool(tmp_items)
        else:
            return config.filled in self


class PcElementInfo(object):
    min_start = -1
    max_end = -1
    next_element = None
    _min_start = None
    _max_start = None

    def __init__(self, index, length, line_length, prev_element=None):
        self.index = index
        self.length = length
        self.line_length = line_length
        self.prev_element = prev_element
        if prev_element is not None:
            self.prev_element.next_element = self

    @property
    def prev_total(self):
        if self.prev_element is None:
            return self.length + 1
        return self.prev_element.prev_total + self.length + 1

    @property
    def next_total(self):
        if self.next_element is None:
            return self.length + 1
        return self.next_element.next_total + self.length + 1

    def calc_starts(self):
        if self.prev_element is None:
            self._min_start = 0
        else:
            self._min_start = self.prev_element.prev_total

        self._max_start = self.line_length - self.length
        if self.next_element is not None:
            self._max_start -= self.next_element.next_total
        if self._max_start < self._min_start:
            raise IndexError(
                'Invalid element position: %r, max: %s, min: %s' % (self, self._max_start, self._min_start))

    @property
    def min_start(self):
        if self._min_start is None:
            self.calc_starts()
        return self._min_start

    @property
    def max_start(self):
        if self._max_start is None:
            self.calc_starts()
        return self._max_start

    def make_range(self, min_start):
        min_start = max(min_start, self.min_start)
        if min_start > self.max_start:
            return []
        return range(min_start, self.max_start + 1)

    def make_list(self, start_pos):
        tmp_ret = PcLineHelper(line_length=self.line_length, is_mask=False)
        if not self.min_start <= start_pos <= self.max_start:
            raise IndexError('%r cannot make a list starting at position %s', (self, start_pos))
        for i in range(start_pos, start_pos + self.length):
            tmp_ret[i] = config.filled
        return tmp_ret

        """
        tmp_ret = [OC.skipped] * self.line_length
        if not self.min_start <= start_pos <= self.max_start:
            raise IndexError('%r cannot make a list starting at position %s', (self, start_pos))
        for i in range(start_pos, start_pos + self.length):
            tmp_ret[i] = OC.filled
        return tmp_ret
        """

    def make_options(self, min_start=0):
        """
        returns ['index', 'index', 'index']
        """
        """
        tmp_ret = []
        for i in self.make_range(min_start):
            tmp_item = self.make_list(i)

            if self.next_element is not None:
                for n in self.next_element.make_options(i + self.length + 1):
                    tmp_item_2 = merge_lists(tmp_item, n)
                    tmp_ret.append(tmp_item_2)
            else:
                tmp_ret.append(tmp_item)
        return tmp_ret
        """
        tmp_ret = []
        for i in self.make_range(min_start):
            tmp_item = self.make_list(i)

            if self.next_element is not None:
                for n in self.next_element.make_options(i + self.length + 1):
                    n.update(tmp_item)
                    tmp_ret.append(n)
            else:
                tmp_ret.append(tmp_item)
        return tmp_ret

    def __repr__(self):
        return f'ElementInfo(index={self.index}, length={self.length})'


class PcLine(object):
    """
    len(pc) -> returns the number of possible filtered lines
    str(pc) -> returns the line_mask in string form.
    as_table() -> returns an html table of the data
    iter(pc) -> iterates the lines as lists of lists.
    as_string() -> returns the information as a string
    header() -> returns an iterable of the header
    data() -> returns an iterable of the data lines
    mask() -> returns an iterable of the mask

    """
    error = None
    is_error = False

    def __init__(self,
                 line_length,
                 elements,
                 mask=None,
                 title_format='Line: {line_number} {knowns} {elements}',
                 header_init_col='',
                 data_init_col='Option {line_no}',
                 mask_init_col='{title}',
                 table_template=None,
                 raise_error=False,
                 replace_values_with=None,
                 line_num=0,
                 ):
        self.replace_values = replace_values_with
        self.line_length = line_length
        self.line_number = line_num
        self.root = None
        self.all_data = []
        self.filtered_data = []
        self.line_mask = None
        self.raise_error = raise_error
        self.title_format = title_format
        self.header_init_col = header_init_col
        self.data_init_col = data_init_col
        self.mask_init_col = mask_init_col
        self.table_template = table_template
        try:
            self.elements = split_string(elements, as_int=True)
            self.knowns = self.make_line(mask, is_mask=True)

            if len(self.knowns) > self.line_length:
                raise PcException(
                    'Too many knowns (%r) to fit in the known line length of %s' % (self.knowns, self.line_length))

            if sum(self.elements) + len(self.elements) - 1 > line_length:
                raise PcException('Element total too long for row')
            prev_element = None
            for i, e in enumerate(self.elements):
                try:
                    tmp_info = PcElementInfo(index=i, length=e, line_length=self.line_length, prev_element=prev_element)
                except IndexError:
                    continue
                if self.root is None:
                    self.root = tmp_info
                prev_element = tmp_info

            self.all_data = self.root.make_options()

            self.filtered_data = []
            for i in self.all_data:
                if i == self.knowns:
                    self.filtered_data.append(i)

            self.line_mask = PcLineHelper(line_length=self.line_length, is_mask=True)

            if not self.filtered_data:
                raise PcException('No options match filter mask.')

            self.line_mask = self.line_mask.make_mask(*self.filtered_data)

        except Exception as err:
            self.is_error = True
            self.error = str(err)
            if raise_error:
                raise

    def make_line(self, items, **kwargs):
        kwargs['line_length'] = self.line_length
        kwargs['replace_values_with'] = self.replace_values
        return PcLineHelper(items, **kwargs)

    def dump(self):
        tmp_ret = [
            f'Line Length: {self.line_length}',
            f'Elements: {repr(self.elements)}',
            f'All Data:',
        ]
        for index, i in enumerate(self.all_data):
            tmp_ret.append(i.format(prefix='Option {line_num}: ', line_num=index + 1, indent_size=4))
        if self.knowns:
            tmp_ret.append('')
            tmp_ret.append(f'Mask In: {self.knowns}')
            tmp_ret.append('Filtered Data:')
            for index, i in enumerate(self.filtered_data):
                tmp_ret.append(i.format(prefix='Filtered {line_num}: ', line_num=index + 1, indent_size=4))
        else:
            tmp_ret.append('Mask In: No Mask Specified')

        tmp_ret.append(f'Final Mask: {self.line_mask}')

        return '\n'.join(tmp_ret)

    def as_iter(self, inc_data=True, inc_header=True, inc_mask=True, init_col=True, alt_values=None):
        tmp_ret = []
        if inc_header:
            tmp_ret.append(self.header(init_col=init_col))
        if inc_data:
            tmp_ret.extend(self.data(init_col=init_col, alt_values=alt_values))
        if inc_mask:
            tmp_ret.append(self.mask(init_col=init_col, alt_values=alt_values))
        return tmp_ret

    def as_string(self, inc_data=True, inc_header=True, inc_mask=True, init_col=True, sep='', line_sep='\n'):
        tmp_ret = []
        if inc_header:
            for l in self.split_vert_headers(init_col=init_col):
                tmp_ret.append(sep.join(l))
        if inc_data:
            for l in self.data(init_col=init_col):
                tmp_ret.append(sep.join(l))
        if inc_mask:
            tmp_ret.append(sep.join(self.mask(init_col=init_col)))

        tmp_ret = line_sep.join(tmp_ret)

        return tmp_ret

    def split_vert_headers(self, init_col=True):

        init_col = bol_or_str(init_col, self.header_init_col)
        tmp_rng = list(range(1, self.line_length + 1))
        max_digits = num_digits(tmp_rng[-1])
        tmp_rng = map(str, tmp_rng)

        if max_digits == 1:
            return [list(tmp_rng)]

        lines = []
        for i in range(max_digits):
            lines.append([])

        for item in tmp_rng:
            for index in range(max_digits):
                lines[index].append(item[index])

        if init_col is not None:
            for l in lines:
                l.insert(0, '')
            lines[0][0] = init_col

        return lines

    def header(self, init_col=True):
        header = []
        init_col = bol_or_str(init_col, self.header_init_col)

        if init_col is not None:
            header.append(init_col)

        for c in range(1, self.line_length + 1):
            h = str(c)
            header.append(h)
        return header

    def data(self, init_col=True):
        init_col = bol_or_str(init_col, self.data_init_col)
        if init_col is None:
            return self.filtered_data
        else:
            tmp_ret = []
            for index, row in enumerate(self.filtered_data):
                tmp_row = row.copy()
                if init_col:
                    ic = self.fmt(init_col, index0=index, index1=index + 1)
                    tmp_row.insert(0, ic)
                tmp_ret.append(tmp_row)
            return tmp_ret

    def mask(self, init_col=True):
        """
        returns the final mask (all overlapping positions)
        :param init_col:
        :return:
        """
        mask = []
        init_col = bol_or_str(init_col, self.header_init_col)
        if init_col is not None:
            fs = self.fmt(init_col)
            mask.append(fs)
        mask.extend(self.line_mask)
        return mask

    def fmt(self, fmt_str, from_title=False, **kwargs):
        """
        returns a formatted string using common keys
        :param fmt_str:
        :param from_title:
        :param kwargs:
        :return:
        """
        kwargs.update(dict(
            knowns=repr(self.knowns),
            elements=repr(self.elements),
            line_length=self.line_length,
            element_count=len(self.elements),
            count=len(self),
            line_number=self.line_number,
        ))
        if not from_title:
            kwargs['title'] = self.title(),

        tmp_ret = fmt_str.format(**kwargs)
        return tmp_ret

    def title(self, fmt=None):
        fmt = fmt or self.title_format
        return self.fmt(fmt, from_title=True)

    def __len__(self):
        return len(self.filtered_data)

    def __repr__(self):
        try:
            return self.title()
        except Exception:
            return 'PcLine (in error: %s)' % self.error


class PcMatrix(object):
    def __init__(self,
                 line_length,
                 line_count,
                 lines,
                 **kwargs):
        """

        :param line_length: the length of each line
        :param lines:
            either list or dict in the form of:
                list: [
                        {
                            'mask': ['X', '0', '.', ...],
                            'elements': '3','4','5','6', ...],
                        },
                        ...
                        ]
                dict:
                    {
                        'l1': '1,2,3,4',
                        'l1m0': 'x',
                        'l1m1': '0',
                    }

        """
        self.line_count = line_count
        self.line_length = line_length
        self.kwargs = kwargs
        # if not isinstance(lines, list):
        #     lines = convert_element_dict_to_list(lines, line_length=line_length, row_count=line_count)
        self.line_data = lines
        self.lines = []
        for l in lines:
            l.update(kwargs)
            tmp_line = PcLine(**l)
            self.lines.append(tmp_line)

    def __iter__(self):
        for i in self.lines:
            yield i

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, item):
        return self.lines[item]
