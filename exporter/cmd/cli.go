package main

import (
	"log/slog"

	"orgfin.run/exporter/internal/config"
	logger "orgfin.run/exporter/internal/logger"
)

func main() {
	cfg, err := config.New("")
	if err != nil {
		slog.Error("Failed to load config", "error", err)
		return
	}

	logger.Init("dev")

	slog.Info("Config: ", slog.Any("config", cfg))
}
