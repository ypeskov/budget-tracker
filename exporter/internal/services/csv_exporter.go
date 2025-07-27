package services

import (
	"encoding/csv"
	"fmt"
	"log/slog"
	"os"
	"time"

	"orgfin.run/exporter/internal/models"
)

type CSVExporterInstance struct {
	transactions []models.Transaction
}

type CSVExporter interface {
	// ExportToCSV exports the transactions to a CSV file.
	// It creates a new CSV file with the current date and time in the filename.
	// It writes the transactions to the CSV file.
	ExportToCSV(transactions []models.Transaction) error
}

func NewCSVExporter(transactions []models.Transaction) CSVExporter {
	return &CSVExporterInstance{transactions: transactions}
}

// ExportToCSV exports the transactions to a CSV file.
// It creates a new CSV file with the current date and time in the filename.
// It writes the transactions to the CSV file.
func (c *CSVExporterInstance) ExportToCSV(transactions []models.Transaction) error {
	fileName := fmt.Sprintf("transactions_%s.csv", time.Now().Format("2006-01-02_15-04-05"))
	slog.Info("Exporting to CSV...", "file", fileName)
	csvFile, err := os.Create(fileName)
	if err != nil {
		slog.Error("Failed to create csv file", "error", err)
		return err
	}
	defer csvFile.Close()

	csvWriter := csv.NewWriter(csvFile)

	if err := csvWriter.Write([]string{"ID", "User ID", "Date Time", "Amount", "Category ID",
		"Label", "Amount In Base", "Currency", "Base Currency"}); err != nil {
		slog.Error("Failed to write header", "error", err)
		return err
	}

	for _, transaction := range transactions {
		if err := csvWriter.Write([]string{transaction.ID, transaction.UserID, transaction.DateTime,
			fmt.Sprintf("%f", transaction.Amount), fmt.Sprintf("%d", transaction.CategoryID.Int64),
			transaction.Label.String, fmt.Sprintf("%f", transaction.AmountInBase.Float64),
			transaction.Currency.String, transaction.BaseCurrency.String}); err != nil {
			slog.Error("Failed to write transaction", "error", err)
			return err
		}
	}

	csvWriter.Flush()
	if err := csvWriter.Error(); err != nil {
		slog.Error("Failed to flush csv writer", "error", err)
		return err
	}

	slog.Info("CSV file created", "file", fileName)
	return nil
}
