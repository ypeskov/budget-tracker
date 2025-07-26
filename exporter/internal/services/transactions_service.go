package services

import (
	"orgfin.run/exporter/internal/models"
	"orgfin.run/exporter/internal/respositories"
)

type TransactionsService struct {
	transactionsRepository respositories.Transaction
}

type Transaction interface {
	// GetAllForUser gets all transactions for a user.
	// It returns a slice of transactions and an error if
	// the transactions cannot be fetched.
	GetAllForUser(userID int64) ([]models.Transaction, error)
}

// NewTransactionsService creates a new TransactionsService.
func NewTransactionsService(transactionsRepository respositories.Transaction) Transaction {
	return &TransactionsService{transactionsRepository: transactionsRepository}
}

func (s *TransactionsService) GetAllForUser(userID int64) ([]models.Transaction, error) {
	return s.transactionsRepository.GetAllForUser(userID)
}
