package api

import (
	"os"
	"strings"
	"testing"
)
var data, _ = os.ReadFile("../../data/kp_table.txt")

func TestParse_TabsInData(t *testing.T) {
	// ensure that tabs are treated as fields
	raw := []byte(strings.Join([]string{
		"Some header",
		"NOAA Kp index breakdown",
		"",
		"Apr\t10\tApr\t11\tApr\t12",
		"00-03\t2.0\t2.1\t2.2",
		"03-06\t2.5\t2.6\t2.7",
		"06-09\t2.0\t2.1\t2.2",
		"09-12\t2.5\t2.6\t2.7",
		"12-15\t2.0\t2.1\t2.2",
		"15-18\t2.5\t2.6\t2.7",
		"18-21\t2.0\t2.1\t2.2",
		"21-24\t2.5\t2.6\t2.7",
	}, "\n"))
	fc, err := parse(raw)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(fc.Dates) != 3 {
		t.Errorf("dates len: want 3, got %d", len(fc.Dates))
	}
	if len(fc.TimePeriods) != 8 {
		t.Errorf("time periods len: want 8, got %d", len(fc.TimePeriods))
	}
	if len(fc.Values) != 8 {
		t.Errorf("values rows: want 2, got %d", len(fc.Values))
	}
}

func TestParse_PanicOnInsufficientLines(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("expected panic due to insufficient data lines, got none")
		}
	}()
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown",
		"",
		"Apr 10 Apr 11 Apr 12 Apr 13 Apr 14",
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
		"",
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
		"",
		"Apr 10 Apr 11 Apr 12",
		"00-03      2.33   2.67   XX",
		"03-06      2.67   3.00   3.33",
		"06-09      2.00   2.33   2.67",
		"09-12      2.33   X   3.00",
		"12-15      2.67   3.00   3.33",
		"15-18      2.00   2.33   2.67",
		"18-21      2.33   2.67   3.00",
		"21-24      2.67   3.00   3.33",
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
		"",
		"Apr 10 Apr 11 Apr 12",
		"",
		"00-03      2.33   2.67   3.00",
		"",
		"03-06      2.67   3.00   3.33",
		"",
		"06-09      2.33   2.67   3.00",
		"",
		"09-12      2.67   3.00   3.33",
		"",
		"",
	}, "\n"))
	forecast, err := parse(raw)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(forecast.TimePeriods) != 4 {
		t.Errorf("expected 4 time periods, got %d", len(forecast.TimePeriods))
	}
}

func TestParse_ShortDataLines(t *testing.T) {
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown Short Data Lines",		
		"Apr 10 Apr 11 Apr 12 Apr 13",
		"",
		"00-03      2.33   2.67",
		"03-06      2.33   2.67",
		"06-09      2.33   2.67",
		"09-12      2.33   2.67",
		"12-15      2.33   2.67",
		"15-18      2.33   2.67",
		"18-21      2.33   2.67",
		"21-24      2.33   2.67",
		"21-24      2.33   2.67",
	}, "\n"))
	_, err := parse(raw)
	if err == nil {
		t.Error("expected error due to short data line, got nil")
	}
}

func TestParse_Success(t *testing.T) {
	fc, err := parse(data)
	if err != nil {
		t.Fatalf("parse failed: %v", err)
	}
	wantDates := []string{"Dec-30", "Dec-31", "Jan-01"}
	if len(fc.Dates) != 3 {
		t.Errorf("expected 3 dates, got %d", len(fc.Dates))
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
	if fc.Values[0][0] != 1 || fc.Values[7][2] != 3 {
		t.Errorf("unexpected values: got %v", fc.Values)
	}
}

func TestParse_NonNumericValue(t *testing.T) {
	raw := []byte(strings.Join([]string{
		"NOAA Kp index breakdown Non Numeric",
		"",
		"May 24 May 25 May 26",
		"00-03 2.0 2.3 X",
		"03-06 2.1 2.4 2.6",
		"06-09 2.0 2.1 AWE",
		"09-12 2.5 2.6 2.7",
		"12-15 2.0 2.1 2.2",
		"15-18 2.5 #4f$ 2.7",
		"18-21 2.0 2.1 2.2",
		"21-24 2.5 2.6 2.7",
	}, "\n"))
	_, err := parse(raw)
	if err == nil || !strings.Contains(err.Error(), "parse") {
		t.Errorf("expected parse error, got %v", err)
	}
}

func TestFetchForecast_Success (t *testing.T) {
	fc, err := FetchForecast()
	if err != nil {
		t.Fatalf("FetchForecast failed: %v", err)
	}
	if len(fc.Dates) != 3 {
		t.Errorf("expected 3 dates, got %d", len(fc.Dates))
	}
	if len(fc.TimePeriods) != 8 {
		t.Errorf("expected 8 time periods, got %d", len(fc.TimePeriods))
	}
	if len(fc.Values) != 8 {
		t.Errorf("expected 8 value rows, got %d", len(fc.Values))
	}
}
