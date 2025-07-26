package main

import (
	"fmt"
	"log/slog"
	"os"

	"github.com/spf13/cobra"

	"orgfin.run/exporter/internal/config"
	"orgfin.run/exporter/internal/database"
	logger "orgfin.run/exporter/internal/logger"
	"orgfin.run/exporter/internal/models"
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

	transactions := []models.Transaction{}
	query := `
	SELECT id, user_id, date_time, amount, category_id, label
	FROM transactions
	WHERE user_id = $1
	ORDER BY date_time DESC
	LIMIT 10
	`
	err = db.Db.Select(&transactions, query, "1")
	if err != nil {
		slog.Error("Failed to select transactions", "error", err)
		return
	}

	for _, transaction := range transactions {
		fmt.Printf("Transaction: %s\n", transaction.ID)
		fmt.Printf("  User ID: %s\n", transaction.UserID)
		fmt.Printf("  Date Time: %s\n", transaction.DateTime)
		fmt.Printf("  Amount: %f\n", transaction.Amount)
		fmt.Printf("  Category ID: %d\n", transaction.CategoryID.Int64)
		fmt.Printf("  Label: %s\n", transaction.Label.String)
		fmt.Printf("  Amount In Base: %f\n", transaction.AmountInBase.Float64)
		fmt.Printf("  Currency: %s\n", transaction.Currency.String)
		fmt.Println("--------------------------------")
	}
}
