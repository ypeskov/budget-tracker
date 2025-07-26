package main

import (
	"encoding/csv"
	"fmt"
	"log/slog"
	"os"
	"strconv"

	"github.com/spf13/cobra"

	"orgfin.run/exporter/internal/config"
	"orgfin.run/exporter/internal/database"
	logger "orgfin.run/exporter/internal/logger"
	"orgfin.run/exporter/internal/models"
	"orgfin.run/exporter/internal/respositories"
	"orgfin.run/exporter/internal/services"
)

var envFile string
var userID string

var rootCmd = &cobra.Command{
	Use: "exporter",
}

func main() {
	rootCmd.PersistentFlags().StringVarP(&userID, "uid", "u", "1", "user id")
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

	db, err := database.New(cfg)
	if err != nil {
		slog.Error("Failed to connect to database", "error", err)
		return
	}

	slog.Info("App initialized")

	run(db)
}

func run(db *database.Database) {
	slog.Info("Running app...")

	userIDInt, err := strconv.ParseInt(userID, 10, 64)
	if err != nil {
		slog.Error("Failed to parse user id", "error", err)
		return
	}

	slog.Info("Getting transactions...")
	transactionsRepository := respositories.NewTransactionsRepository(db)
	transactionsService := services.NewTransactionsService(transactionsRepository)

	transactions, err := transactionsService.GetAllForUser(userIDInt)
	if err != nil {
		slog.Error("Failed to get all transactions for user", "error", err)
		return
	}
	slog.Info("Transactions fetched", "count", len(transactions))

	slog.Info("Exporting to CSV...")
	exportToCSV(transactions)
	slog.Info("CSV exported")
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
