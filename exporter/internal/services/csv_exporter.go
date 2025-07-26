package services

import (
	"encoding/csv"
	"fmt"
	"log/slog"
	"os"
	"time"

	"orgfin.run/exporter/internal/models"
)

// ExportToCSV exports the transactions to a CSV file.
// It creates a new CSV file with the current date and time in the filename.
// It writes the transactions to the CSV file.
func ExportToCSV(transactions []models.Transaction) {
	fileName := fmt.Sprintf("transactions_%s.csv", time.Now().Format("2006-01-02_15-04-05"))
	slog.Info("Exporting to CSV...", "file", fileName)
	slog.Info("Creating CSV file")
	csvFile, err := os.Create(fileName)
	if err != nil {
		slog.Error("Failed to create csv file", "error", err)
		return
	}
	defer csvFile.Close()

	csvWriter := csv.NewWriter(csvFile)

	csvWriter.Write([]string{"ID", "User ID", "Date Time", "Amount", "Category ID",
		"Label", "Amount In Base", "Currency", "Base Currency"})
	for _, transaction := range transactions {
		csvWriter.Write([]string{transaction.ID, transaction.UserID, transaction.DateTime,
			fmt.Sprintf("%f", transaction.Amount), fmt.Sprintf("%d", transaction.CategoryID.Int64),
			transaction.Label.String, fmt.Sprintf("%f", transaction.AmountInBase.Float64),
			transaction.Currency.String, transaction.BaseCurrency.String})
	}
	csvWriter.Flush()
	slog.Info("CSV file created", "file", fileName)
}
