package main

import (
	"encoding/csv"
	"fmt"
	"log/slog"
	"os"

	"github.com/spf13/cobra"

	"orgfin.run/exporter/internal/config"
	"orgfin.run/exporter/internal/database"
	logger "orgfin.run/exporter/internal/logger"
	"orgfin.run/exporter/internal/models"
	"orgfin.run/exporter/internal/respositories"
	"orgfin.run/exporter/internal/services"
)

var envFile string

var rootCmd = &cobra.Command{
	Use: "exporter",
}

func main() {
	rootCmd.PersistentFlags().StringVarP(&envFile, "env", "e", ".env", "path to .env file")

	if err := rootCmd.Execute(); err != nil {
		slog.Error("cli failed", "error", err)
		os.Exit(1)
	}

	cfg, err := config.New(envFile)
	if err != nil {
		slog.Error("Failed to load config", "error", err)
		return
	}

	logger.Init(cfg.Env)

	slog.Info("Config: ", slog.Any("config", cfg))

	db, err := database.New(cfg)
	if err != nil {
		slog.Error("Failed to connect to database", "error", err)
		return
	}

	transactionsRepository := respositories.NewTransactionsRepository(db)
	transactionsService := services.NewTransactionsService(transactionsRepository)

	transactions, err := transactionsService.GetAllForUser(1)
	if err != nil {
		slog.Error("Failed to get all transactions for user", "error", err)
		return
	}

	// export to csv
	exportToCSV(transactions)

}

func exportToCSV(transactions []models.Transaction) {
	csvFile, err := os.Create("transactions.csv")
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
}
