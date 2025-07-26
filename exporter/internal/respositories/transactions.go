package respositories

import (
	"log/slog"

	"orgfin.run/exporter/internal/database"
	"orgfin.run/exporter/internal/models"
)

type TransactionsRepository struct {
	db *database.Database
}

type Transaction interface {
	GetAllForUser(userID int64) ([]models.Transaction, error)
}

func NewTransactionsRepository(db *database.Database) Transaction {
	return &TransactionsRepository{db: db}
}

func (r *TransactionsRepository) GetAllForUser(userID int64) ([]models.Transaction, error) {
	query := `
		SELECT id, user_id, date_time, amount, category_id, label
		FROM transactions
		WHERE user_id = $1
		ORDER BY date_time ASC
	`
	transactions := []models.Transaction{}
	err := r.db.Db.Select(&transactions, query, userID)
	if err != nil {
		slog.Error("Failed to get all transactions for user", "error", err)
		return nil, err
	}
	return transactions, nil
}
