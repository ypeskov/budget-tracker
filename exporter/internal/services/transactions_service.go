package services

import (
	"orgfin.run/exporter/internal/models"
	"orgfin.run/exporter/internal/respositories"
)

type TransactionsService struct {
	transactionsRepository respositories.Transaction
}

type Transaction interface {
	GetAllForUser(userID int64) ([]models.Transaction, error)
}

func NewTransactionsService(transactionsRepository respositories.Transaction) Transaction {
	return &TransactionsService{transactionsRepository: transactionsRepository}
}

func (s *TransactionsService) GetAllForUser(userID int64) ([]models.Transaction, error) {
	return s.transactionsRepository.GetAllForUser(userID)
}
