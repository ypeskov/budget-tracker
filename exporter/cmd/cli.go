package main

import (
	"log/slog"
	"os"

	"github.com/spf13/cobra"

	"orgfin.run/exporter/internal/config"
	logger "orgfin.run/exporter/internal/logger"
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
}
