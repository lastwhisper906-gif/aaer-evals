import contextlib
import io
import json

import power_analysis


def capture(args):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        power_analysis.main(args)
    return output.getvalue()


def test_deterministic_output():
    assert capture([]) == capture([])
    assert capture(["--json"]) == capture(["--json"])


def test_required_n_sanity():
    easy = power_analysis.required_n(0.83, 0.50, 1.0, 0.05, 0.80)
    close = power_analysis.required_n(0.83, 0.65, 1.0, 0.05, 0.80)
    assert 5 <= easy[0] <= 40
    assert easy[0] < close[0]


def test_inverse_normal_round_trip():
    grid = [1e-6, 1e-4, 0.001, 0.01, 0.1, 0.25, 0.5,
            0.75, 0.9, 0.99, 0.999, 0.9999, 1.0 - 1e-6]
    errors = [abs(power_analysis.normal_cdf(power_analysis.normal_ppf(p)) - p)
              for p in grid]
    assert max(errors) < power_analysis.INV_CDF_ROUNDTRIP_MAX_ERROR


def test_achieved_power_monotonic_in_n():
    powers = [power_analysis.achieved_power(0.83, 0.65, n, n, 0.05)
              for n in (5, 10, 20, 40)]
    assert powers == sorted(powers)
    assert len(set(powers)) == len(powers)


def test_json_matches_printed_table_numbers():
    data = json.loads(capture(["--json"]))
    table = capture([])
    assert data == power_analysis.results()
    for row in data["required_n"]:
        p80, p90 = row["power_0.80"], row["power_0.90"]
        expected = (f'{row["auc1"]:.2f} vs {row["auc0"]:.2f} | {row["ratio"]} | '
                    f'{p80["n_t"]}/{p80["n_c"]}/{p80["total_n"]} | '
                    f'{p90["n_t"]}/{p90["n_c"]}/{p90["total_n"]}')
        assert expected in table
    for row in data["achieved_power"]:
        expected = (f'{row["design"]} | {row["n_t"]}/{row["n_c"]} | '
                    f'{row["0.83_vs_0.50"]:.3f} | {row["0.83_vs_0.65"]:.3f}')
        assert expected in table
