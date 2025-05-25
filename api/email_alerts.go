package api

import (
	"fmt"
	"net/smtp"
	"os"
	"strings"
	"time"

	"github.com/tswiger34/NorthernLightsApp/types"
	"golang.org/x/crypto/bcrypt"
)

func LoadEmailConfigFromEnv() types.EmailConfig {
    return types.EmailConfig{
        SMTPHost:     os.Getenv("SMTP_HOST"),
        SMTPPort:     os.Getenv("SMTP_PORT"),
        SMTPUsername: os.Getenv("SMTP_USERNAME"),
        SMTPPassword: os.Getenv("SMTP_PASSWORD"),
        FromEmail:    os.Getenv("FROM_EMAIL"),
    }
}

func HashPassword(password string) (string, error) {
    hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    return string(hash), err
}

func FormatResults(fc *types.Forecast) ([]string, error) {
	if fc == nil || len(fc.Values) == 0 {
		return nil, fmt.Errorf("no forecast data available")
	}
	var results []string
	for i, kp_row := range fc.Values {
		for j, kp_val := range kp_row {
			if kp_val >= 5.0 {
				results = append(results, fmt.Sprintf("Northern lights expected on %s during %s with Kp value %.2f", fc.Dates[j], fc.TimePeriods[i], kp_val))
			}
		}
	}
	if len(results) == 0 {
		return []string{fmt.Sprintf("The northern lights will not be visible between %s and %s", fc.Dates[0], fc.Dates[2])}, nil
	}
	return results, nil
}

func SendDailyReport(config types.EmailConfig, toEmail string, fc *types.Forecast) error {
	// Format the results
	results, err := FormatResults(fc)
	if err != nil {
		return fmt.Errorf("failed to format results: %w", err)
	}

	// Create subject line with today's date
	subject := fmt.Sprintf("Daily Northern Lights Report for %s", time.Now().Format("January 2, 2006"))

	// Create email body
	body := strings.Join(results, "\n")
	if len(results) > 1 {
		body = "Here are the northern lights predictions:\n\n" + body
	}

	// Create the email message
	message := fmt.Sprintf("To: %s\r\nSubject: %s\r\n\r\n%s", toEmail, subject, body)

	// Send the email
	auth := smtp.PlainAuth("", config.SMTPUsername, config.SMTPPassword, config.SMTPHost)
	err = smtp.SendMail(
		config.SMTPHost+":"+config.SMTPPort,
		auth,
		config.FromEmail,
		[]string{toEmail},
		[]byte(message),
	)
	if err != nil {
		return fmt.Errorf("failed to send email: %w", err)
	}

	return nil
}

func SendDailyReportToMultiple(config types.EmailConfig, toEmails []string, fc *types.Forecast) error {
	for _, email := range toEmails {
		if err := SendDailyReport(config, email, fc); err != nil {
			return fmt.Errorf("failed to send email to %s: %w", email, err)
		}
	}
	return nil
}
