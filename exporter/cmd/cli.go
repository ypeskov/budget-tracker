package main

import (
	"log/slog"
	"os"
	"strconv"

	"github.com/spf13/cobra"

	"orgfin.run/exporter/internal/config"
	"orgfin.run/exporter/internal/database"
	logger "orgfin.run/exporter/internal/logger"
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

	slog.Info("App finished")
}

// The main function that runs the app.
// It gets the transactions for the user and exports them to a CSV file.
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

	services.ExportToCSV(transactions)
}
