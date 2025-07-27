package main

import (
	"flag"
	"log/slog"
	"os"
	"strconv"

	"orgfin.run/exporter/internal/config"
	"orgfin.run/exporter/internal/database"
	logger "orgfin.run/exporter/internal/logger"
	"orgfin.run/exporter/internal/models"
	"orgfin.run/exporter/internal/respositories"
	"orgfin.run/exporter/internal/services"
)

func main() {
	userID := flag.String("uid", "1", "user id")
	envFile := flag.String("env", ".env", "path to .env file")

	flag.Parse()

	cfg, err := config.New(*envFile)
	if err != nil {
		slog.Error("Failed to load config", "error", err)
		os.Exit(1)
	}

	logger.Init(cfg)

	db, err := database.New(cfg)
	if err != nil {
		slog.Error("Failed to connect to database", "error", err)
		os.Exit(1)
	}

	slog.Info("App initialized")

	if err := run(db, *userID); err != nil {
		slog.Error("Failed to run app", "error", err)
		os.Exit(1)
	}

	slog.Info("App finished successfully")
}

// The main function that runs the app.
// It gets the transactions for the user and exports them to a CSV file.
func run(db *database.Database, userID string) error {
	slog.Info("Running app...")

	userIDInt, err := strconv.ParseInt(userID, 10, 64)
	if err != nil {
		slog.Error("Failed to parse user id", "error", err)
		return err
	}

	slog.Info("Getting transactions...")
	transactionsRepository := respositories.NewTransactionsRepository(db)
	transactionsService := services.NewTransactionsService(transactionsRepository)

	var transactions []models.Transaction
	if transactions, err = transactionsService.GetAllForUser(userIDInt); err != nil {
		slog.Error("Failed to get all transactions for user", "error", err)
		return err
	}

	slog.Info("Transactions fetched", "count", len(transactions))

	csvExporter := services.NewCSVExporter(transactions)
	if err := csvExporter.ExportToCSV(transactions); err != nil {
		slog.Error("Failed to export transactions to csv", "error", err)
		return err
	}

	slog.Info("Transactions exported to csv")
	return nil
}
