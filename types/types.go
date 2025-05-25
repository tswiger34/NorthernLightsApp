package types

import "time"

type User struct {
	ID       int    `db:"id"`
	Email    string `db:"email"`
	Password string `db:"password_hash"` // Always hash passwords
	Active   bool   `db:"active"`
}

type EmailConfig struct {
	SMTPHost     string
	SMTPPort     string
	SMTPUsername string
	SMTPPassword string
	FromEmail    string
}

type Forecast struct {
	Dates       []string
	TimePeriods []string
	Values      [][]float64
	ScrapedAt   time.Time
}

type ForecastParsed struct {
	Date      string
	TimeFrame string
	KpVal     float64
}