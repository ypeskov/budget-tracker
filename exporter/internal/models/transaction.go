package models

import "database/sql"

type Transaction struct {
	ID           string          `db:"id"`
	UserID       string          `db:"user_id"`
	DateTime     string          `db:"date_time"`
	Amount       float64         `db:"amount"`
	CategoryID   sql.NullInt64   `db:"category_id"`
	Label        sql.NullString  `db:"label"`
	AmountInBase sql.NullFloat64 `db:"base_currency_amount"`
	Currency     sql.NullString  `db:"currency"`
	BaseCurrency sql.NullString  `db:"base_currency"`
}
