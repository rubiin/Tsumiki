import json
import os
import tempfile
import unittest

from utils.functions import (
    celsius_to_fahrenheit,
    check_if_day,
    convert_bytes,
    convert_seconds_to_milliseconds,
    convert_to_12hr_format,
    convert_to_percent,
    deep_merge,
    exclude_keys,
    flatten_dict,
    format_seconds_to_hours_minutes,
    get_relative_time,
    is_valid_gjs_color,
    mix_colors,
    rgb_to_css,
    rgb_to_hex,
    tint_color,
    unique_list,
    uptime,
    write_json_file,
)


class FunctionsTest(unittest.TestCase):
    """Test suite for utility functions in the utils module."""

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(celsius_to_fahrenheit(-40), -40)

    def test_deep_merge(self):
        target = {"a": 1, "b": {"x": 10, "y": 20}}
        data = {"b": {"y": 30, "z": 40}, "c": 3}
        merged = deep_merge(data, target)
        expected = {"a": 1, "b": {"x": 10, "y": 30, "z": 40}, "c": 3}
        self.assertEqual(merged, expected)

    def test_flatten_dict(self):
        d = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
        flat = flatten_dict(d)
        expected = {"a": 1, "b-c": 2, "b-d-e": 3}
        self.assertEqual(flat, expected)

    def test_exclude_keys(self):
        d = {"a": 1, "b": 2, "c": 3}
        filtered = exclude_keys(d, ["b"])
        self.assertEqual(filtered, {"a": 1, "c": 3})

    def test_format_seconds_to_hours_minutes(self):
        self.assertEqual(format_seconds_to_hours_minutes(0), "0 h 00 min")
        self.assertEqual(
            format_seconds_to_hours_minutes(59), "0 h 00 min"
        )  # less than 1 min
        self.assertEqual(
            format_seconds_to_hours_minutes(60), "0 h 01 min"
        )  # exactly 1 min
        self.assertEqual(
            format_seconds_to_hours_minutes(90), "0 h 01 min"
        )  # 1 min 30 sec rounds down to 1 min
        self.assertEqual(
            format_seconds_to_hours_minutes(3600), "1 h 00 min"
        )  # exactly 1 hour
        self.assertEqual(
            format_seconds_to_hours_minutes(3661), "1 h 01 min"
        )  # 1 hour 1 min 1 sec rounds down to 1 h 01 min

    def test_convert_bytes(self):
        # 1024 bytes = 1 KB
        self.assertEqual(convert_bytes(1024, "kb"), "1.0KB")
        # 1048576 bytes = 1 MB
        self.assertEqual(convert_bytes(1024**2, "mb"), "1.0MB")
        # 1073741824 bytes = 1 GB
        self.assertEqual(convert_bytes(1024**3, "gb"), "1.0GB")

        # Test formatting with 2 decimal places
        self.assertEqual(convert_bytes(123456789, "mb", ".2f"), "117.74MB")

    def test_check_if_day(self):
        # Format: "%I:%M %p" e.g. "06:00 AM"
        sunrise = "06:00 AM"
        sunset = "06:00 PM"

        self.assertTrue(check_if_day(sunrise, sunset, "07:00 AM"))
        self.assertFalse(check_if_day(sunrise, sunset, "05:00 AM"))
        self.assertFalse(check_if_day(sunrise, sunset, "07:00 PM"))

        # Case when sunset < sunrise (e.g. polar regions)
        self.assertTrue(check_if_day("10:00 PM", "06:00 AM", "11:00 PM"))
        self.assertFalse(check_if_day("10:00 PM", "06:00 AM", "07:00 AM"))

    def test_convert_to_12hr_format(self):
        self.assertEqual(convert_to_12hr_format("0"), "12:00 AM")
        self.assertEqual(convert_to_12hr_format("300"), "3:00 AM")
        self.assertEqual(convert_to_12hr_format("1200"), "12:00 PM")
        self.assertEqual(convert_to_12hr_format("2100"), "9:00 PM")

    def test_unique_list(self):
        lst = [1, 2, 2, 3, 4, 4, 5]
        result = unique_list(lst)
        self.assertEqual(sorted(result), [1, 2, 3, 4, 5])

    def test_get_relative_time(self):
        self.assertEqual(get_relative_time(0), "now")
        self.assertEqual(get_relative_time(1), "1 minute ago")
        self.assertEqual(get_relative_time(59), "59 minutes ago")
        self.assertEqual(get_relative_time(60), "1 hour ago")
        self.assertEqual(get_relative_time(120), "2 hours ago")
        self.assertEqual(get_relative_time(1440), "1 day ago")
        self.assertEqual(get_relative_time(2880), "2 days ago")

    def test_convert_to_percent(self):
        self.assertEqual(convert_to_percent(50, 100), 50)
        self.assertEqual(convert_to_percent(1, 3, is_int=False), (1 / 3) * 100)
        self.assertEqual(convert_to_percent(0, 0), 0)

    def test_is_valid_gjs_color(self):
        # Assuming NAMED_COLORS is a set or list of color names
        for name in ["red", "blue"]:
            self.assertTrue(is_valid_gjs_color(name))
        self.assertTrue(is_valid_gjs_color("#fff"))
        self.assertTrue(is_valid_gjs_color("#ffffff"))
        self.assertTrue(is_valid_gjs_color("rgb(255, 0, 0)"))
        self.assertTrue(is_valid_gjs_color("rgba(255, 0, 0, 0.5)"))
        self.assertTrue(is_valid_gjs_color("rgb(256, 0, 0)"))
        self.assertFalse(is_valid_gjs_color("invalidcolor"))

    def test_uptime(self):
        # Just test format, it should be HH:MM
        result = uptime()
        self.assertRegex(result, r"^\d{2}:\d{2}$")

    def test_convert_seconds_to_milliseconds(self):
        self.assertEqual(convert_seconds_to_milliseconds(1), 1000)
        self.assertEqual(convert_seconds_to_milliseconds(0), 0)
        self.assertEqual(convert_seconds_to_milliseconds(2), 2000)

    def test_rgb_to_hex(self):
        self.assertEqual(rgb_to_hex((255, 0, 0)), "#ff0000")
        self.assertEqual(rgb_to_hex((0, 255, 0)), "#00ff00")
        self.assertEqual(rgb_to_hex((0, 0, 255)), "#0000ff")
        self.assertEqual(rgb_to_hex((255, 255, 255)), "#ffffff")
        self.assertEqual(rgb_to_hex((0, 0, 0)), "#000000")

    def test_rgb_to_css(self):
        self.assertEqual(rgb_to_css((255, 0, 0)), "rgb(255, 0, 0)")
        self.assertEqual(rgb_to_css((0, 255, 0)), "rgb(0, 255, 0)")
        self.assertEqual(rgb_to_css((0, 0, 255)), "rgb(0, 0, 255)")

    def test_mix_colors_default_ratio(self):
        # 50% red and 50% blue should give purple-ish
        self.assertEqual(mix_colors((255, 0, 0), (0, 0, 255)), (127, 0, 127))

    def test_mix_colors_custom_ratio(self):
        # 25% red and 75% blue
        self.assertEqual(mix_colors((255, 0, 0), (0, 0, 255), ratio=0.75), (63, 0, 191))

    def test_tint_color_full_white(self):
        # Tint factor 1.0 => full white
        self.assertEqual(tint_color((100, 150, 200), 1.0), (255, 255, 255))

    def test_tint_color_no_tint(self):
        # Tint factor 0.0 => original color
        self.assertEqual(tint_color((100, 150, 200), 0.0), (100, 150, 200))

    def test_tint_color_half(self):
        # Tint factor 0.5 => halfway to white
        self.assertEqual(tint_color((0, 0, 0), 0.5), (127, 127, 127))
        self.assertEqual(tint_color((100, 100, 100), 0.5), (177, 177, 177))

    def test_write_json_file(self):
        # Test that write_json_file correctly accepts (path, data) arguments
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            test_data = {"theme": "catppuccin", "version": 1}
            write_json_file(temp_path, test_data)

            # Verify the file was written correctly
            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r") as f:
                loaded_data = json.load(f)
            self.assertEqual(loaded_data, test_data)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
