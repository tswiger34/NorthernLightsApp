package database

import (
	"database/sql"

	"github.com/tswiger34/NorthernLightsApp/types"
)
type DB struct {
	*sql.DB
}

func New(dbPath string) (*DB, error) {
    db, err := sql.Open("sqlite3", dbPath+"?_journal_mode=WAL")
    if err != nil {
        return nil, err
    }
    
    if err := db.Ping(); err != nil {
        return nil, err
    }
    
    return &DB{db}, nil
}

func (db *DB) CreateUser(email, passwordHash string) error {
    _, err := db.Exec(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        email, passwordHash,
    )
    return err
}

func (db *DB) GetUserByEmail(email string) (*types.User, error) {
    var user types.User
    err := db.QueryRow(
        "SELECT id, email, password_hash, active FROM users WHERE email = ?",
        email,
    ).Scan(&user.ID, &user.Email, &user.Password, &user.Active)
    return &user, err
}