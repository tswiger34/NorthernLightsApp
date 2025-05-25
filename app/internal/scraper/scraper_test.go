//go:build unit

package scraper

import (
	"strings"
	"testing"
)

func sampleNOAAData() []byte {
	return []byte(strings.Join([]string{
		"Some header info",
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"00-03      2.33   2.67   3.00   2.33   2.00",
		"03-06      2.67   3.00   3.33   2.67   2.33",
		"06-09      3.00   3.33   3.67   3.00   2.67",
		"09-12      2.67   3.00   3.33   2.67   2.33",
		"12-15      2.33   2.67   3.00   2.33   2.00",
		"15-18      2.00   2.33   2.67   2.00   1.67",
		"18-21      1.67   2.00   2.33   1.67   1.33",
		"21-00      1.33   1.67   2.00   1.33   1.00",
	}, "\n"))
}

func TestParse_ValidData(t *testing.T) {
	raw := sampleNOAAData()
	forecast, err := parse(raw)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(forecast.Dates) != 5 {
		t.Errorf("expected 5 dates, got %d", len(forecast.Dates))
	}
	if len(forecast.TimePeriods) != 8 {
		t.Errorf("expected 8 time periods, got %d", len(forecast.TimePeriods))
	}
	if len(forecast.Values) != 8 {
		t.Errorf("expected 8 rows of values, got %d", len(forecast.Values))
	}
	if forecast.ScrapedAt.IsZero() {
		t.Error("expected ScrapedAt to be set")
	}
}

func TestParse_HeaderNotFound(t *testing.T) {
	raw := []byte("no relevant header here\nsome data\n")
	_, err := parse(raw)
	if err == nil || !strings.Contains(err.Error(), "header not found") {
		t.Errorf("expected header not found error, got %v", err)
	}
}

func TestParse_MalformedData(t *testing.T) {
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"00-03      2.33   2.67   XX   2.33   2.00",
	}, "\n"))
	_, err := parse(raw)
	if err == nil || !strings.Contains(err.Error(), "parse") {
		t.Errorf("expected parse error, got %v", err)
	}
}

// For FetchForecast, we can only test integration if the network is available.
// For a pure unit test, you would refactor FetchForecast to allow injecting a fetcher/mocking colly.

func TestParse_EmptyLines(t *testing.T) {
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"",
		"00-03      2.33   2.67   3.00   2.33   2.00",
		"",
		"03-06      2.67   3.00   3.33   2.67   2.33",
	}, "\n"))
	forecast, err := parse(raw)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(forecast.TimePeriods) != 2 {
		t.Errorf("expected 2 time periods, got %d", len(forecast.TimePeriods))
	}
}

func TestParse_ShortDataLines(t *testing.T) {
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"00-03      2.33   2.67   3.00", // too short
	}, "\n"))
	_, err := parse(raw)
	if err == nil {
		t.Error("expected error due to short data line, got nil")
	}
}

// Sample NOAA forecast text (truncated and simplified for test)
const sampleForecast = `
Some header
NOAA Kp index breakdown
-----------------------
	  06-24 06-25 06-26 06-27 06-28
00-03   2.0   2.3   2.7   2.5   2.2
03-06   2.1   2.4   2.8   2.6   2.3
06-09   2.2   2.5   2.9   2.7   2.4
09-12   2.3   2.6   3.0   2.8   2.5
12-15   2.4   2.7   3.1   2.9   2.6
15-18   2.5   2.8   3.2   3.0   2.7
18-21   2.6   2.9   3.3   3.1   2.8
21-00   2.7   3.0   3.4   3.2   2.9
`

func TestParse_Success(t *testing.T) {
	raw := []byte(sampleForecast)
	fc, err := parse(raw)
	if err != nil {
		t.Fatalf("parse failed: %v", err)
	}
	wantDates := []string{"06-24", "06-25", "06-26", "06-27", "06-28"}
	if len(fc.Dates) != 5 {
		t.Errorf("expected 5 dates, got %d", len(fc.Dates))
	}
	for i, d := range wantDates {
		if fc.Dates[i] != d {
			t.Errorf("date %d: want %q, got %q", i, d, fc.Dates[i])
		}
	}
	if len(fc.TimePeriods) != 8 {
		t.Errorf("expected 8 time periods, got %d", len(fc.TimePeriods))
	}
	if len(fc.Values) != 8 {
		t.Errorf("expected 8 value rows, got %d", len(fc.Values))
	}
	if fc.Values[0][0] != 2.0 || fc.Values[7][4] != 2.9 {
		t.Errorf("unexpected values: got %v", fc.Values)
	}
}

func TestParse_NonNumericValue(t *testing.T) {
	raw := []byte(`
NOAA Kp index breakdown
-----------------------
06-24 06-25 06-26 06-27 06-28
00-03 2.0 2.3 X 2.5 2.2
`)
	_, err := parse(raw)
	if err == nil || !contains(err.Error(), "parse") {
		t.Errorf("expected parse error, got %v", err)
	}
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > 0 && contains(s[1:], substr))
}