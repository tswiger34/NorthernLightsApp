package scraper

import (
	"strings"
	"testing"
)

func TestParse_MissingSeparator(t *testing.T) {
	// header exists but separator line is missing, so idx stays zero
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"00-03 2.0 2.1 2.2 2.3 2.4",
	}, "\n"))
	_, err := parse(raw)
	if err == nil || !strings.Contains(err.Error(), "header not found") {
		t.Errorf("expected header not found error, got %v", err)
	}
}

func TestParse_LowercaseHeader(t *testing.T) {
	// header is lowercase, parse is case‐sensitive, so header not found
	raw := []byte(strings.Join([]string{
		"noaa kp index breakdown",
		"----------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		"00-03 2.0 2.1 2.2 2.3 2.4",
	}, "\n"))
	_, err := parse(raw)
	if err == nil || !strings.Contains(err.Error(), "header not found") {
		t.Errorf("expected header not found error for lowercase header, got %v", err)
	}
}

func TestParse_TabsInData(t *testing.T) {
	// ensure that tabs are treated as fields
	raw := []byte(strings.Join([]string{
		"Some header",
		"NOAA Kp index breakdown",
		"----------",
		"Apr\t10\tApr\t11\tApr\t12\tApr\t13\tApr\t14",
		"00-03\t2.0\t2.1\t2.2\t2.3\t2.4",
		"03-06\t2.5\t2.6\t2.7\t2.8\t2.9",
	}, "\n"))
	fc, err := parse(raw)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(fc.Dates) != 5 {
		t.Errorf("dates len: want 5, got %d", len(fc.Dates))
	}
	if len(fc.TimePeriods) != 2 {
		t.Errorf("time periods len: want 2, got %d", len(fc.TimePeriods))
	}
	if len(fc.Values) != 2 {
		t.Errorf("values rows: want 2, got %d", len(fc.Values))
	}
}

func TestParse_PanicOnInsufficientLines(t *testing.T) {
	// when there aren't enough lines after header+separator+dates,
	// the slice bounds will panic
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic due to insufficient data lines, got none")
		}
	}()
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
		// no data lines at all
	}, "\n"))
	parse(raw)
}

func TestParse_IncompleteDatePairs(t *testing.T) {
	// dates line has fewer than 10 tokens (5 pairs), expecting a panic on slice bounds
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic due to incomplete date fields, got none")
		}
	}()
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"------------------------",
		"Apr 10 Apr 11 Apr 12", // only 3 tokens, not 10
		"00-03 2.0 2.1 2.2",
	}, "\n"))
	parse(raw)
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