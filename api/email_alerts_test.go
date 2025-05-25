package api

import (
	"strings"
	"testing"
	"time"

	"github.com/tswiger34/NorthernLightsApp/types"
)

func TestFormatResults_Success_PositiveA(t *testing.T) {
	sample := types.Forecast{
		Dates:       []string{"May-25", "May-26th", "May-27th"},
		TimePeriods: []string{"00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"},
		Values:      [][]float64{{7, 2, 2}, {2, 2.67, 2.67}, {2, 2.67, 2.67}, {2.67, 2, 1.67}, {2, 1.67, 1.67}, {1, 1, 1}, {1, 1.67, 1}, {1.67, 1.67, 2.67}},
		ScrapedAt:   time.Now().UTC(),
	}

	body, err := FormatResults(&sample)

	if err != nil {
		t.Fatalf("Email Body Formatting Failed: %v", err)
	}
	if len(body) != 1 {
		t.Fatalf("Message body not formatted correctly, expected a length of 1, received length of: %d", len(body))
	}
	if !strings.Contains(body[0], "Northern lights expected on") {
		t.Fatalf("Message body not formatted correctly, expected a message containing `Northern lights expected on`, received %s", body[0])
	}
}

func TestFormatResults_Success_PositiveB(t *testing.T) {
	sample := types.Forecast{
		Dates:       []string{"May-25", "May-26th", "May-27th"},
		TimePeriods: []string{"00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"},
		Values:      [][]float64{{7, 2, 2}, {2, 2.67, 5}, {2, 2.67, 2.67}, {2.67, 5.00, 5.3}, {2, 6, 1.67}, {1, 1, 4.3}, {1, 1.67, 1}, {1.67, 1.67, 2.67}},
		ScrapedAt:   time.Now().UTC(),
	}

	body, err := FormatResults(&sample)

	if err != nil {
		t.Fatalf("Email Body Formatting Failed: %v", err)
	}
	if len(body) != 5 {
		t.Fatalf("Message body not formatted correctly, expected a length of 5, received length of: %d", len(body))
	}
	if !strings.Contains(body[0], "Northern lights expected on") {
		t.Fatalf("Message body not formatted correctly, expected a message containing `Northern lights expected on`, received %s", body[0])
	}
}

func TestFormatResults_Success_NegativeA(t *testing.T) {
	sample := types.Forecast{
		Dates:       []string{"May-25", "May-26th", "May-27th"},
		TimePeriods: []string{"00-03UT", "03-06UT", "06-09UT", "09-12UT", "12-15UT", "15-18UT", "18-21UT", "21-00UT"},
		Values:      [][]float64{{2, 2, 2}, {2, 2.67, 2}, {2, 2.67, 2.67}, {2.67, 2, 2}, {2, 2, 1.67}, {1, 1, 4.3}, {1, 1.67, 1}, {1.67, 1.67, 2.67}},
		ScrapedAt:   time.Now().UTC(),
	}

	body, err := FormatResults(&sample)

	if err != nil {
		t.Fatalf("Email Body Formatting Failed: %v", err)
	}
	if len(body) != 1 {
		t.Fatalf("Message body not formatted correctly, expected a length of 1, received length of: %d", len(body))
	}
	if !strings.Contains(body[0], "The northern lights will not") {
		t.Fatalf("Message body not formatted correctly, expected a message containing `Northern lights expected on`, received %s", body[0])
	}
}