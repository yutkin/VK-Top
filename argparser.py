import argparse
import textwrap
import sys
import const


def parse_args():
    descr = textwrap.dedent('''\
    Script shows posts of any public availabe page at VK.com
    Posts sorted by likes or reposts in the descending order.
    Github: https://github.com/yutkin/VK-Top

    Possible types of input URLs:
    * https://vk.com/page_name
    * http://vk.com/club12345
    * public1234567
    * id1234567
    * event1234567
    '''.format(progname=sys.argv[0]))

    parser = argparse.ArgumentParser(description=descr,
                           formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('url', help='target page', type=check_value_of_url_arg)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-l', '--likes', help='sort posts by likes (by default)',
                       action='store_true', default=True)
    group.add_argument('-r', '--reposts', help='sort posts by reposts',
                       action='store_true')

    parser.add_argument('-t', '--top', help='number of showing posts. (10 by default)',
                        default=10, type=check_value_for_positive_int)

    parser.add_argument('-d', '--days', type=int, default=-1,
                        help='last period (in days) for post processing. (all period by default)')

    return parser.parse_args()


def check_value_of_url_arg(val):

    txt_id = const.TXT_ID_REGEXP.match(val.lower())
    num_id = const.NUM_ID_REGEXP.match(val.lower())

    if txt_id:
        tmp_dict = txt_id.groupdict()
        tmp_dict['type'] = 'symbolic'
        return tmp_dict
    elif num_id:
        return num_id.groupdict()
    else:
        msg = '"{0}" is not acceptable URL'.format(val)
        raise argparse.ArgumentTypeError(msg)


def check_value_for_positive_int(val):
    try:
        num = int(val)
        if num >= 0:
            return num
        else:
            raise ValueError
    except ValueError:
        msg = '{0} invalid argument'.format(val)
        raise argparse.ArgumentTypeError(msg)
