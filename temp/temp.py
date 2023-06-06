import re
contents = '''============================= test session starts ==============================
platform linux -- Python 3.8.10, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: /home/ci/tests/otg_uhd_automation/tests/systemTest
plugins: html-3.2.0, metadata-1.11.0
collected 3 items / 2 deselected / 1 selected

tests/protocols/test_bgp.py .                                            [100%]

================= 1 passed, 2 deselected in 125.28s (0:02:05) ==================
'''

match = re.search(r'(\d+) passed', contents)
if match :
    passed_count = int(match.group(1))
    print(passed_count)