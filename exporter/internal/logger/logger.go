package logger

import (
	"log/slog"
	"os"
	"strings"

	"github.com/lmittmann/tint"
	"orgfin.run/exporter/internal/config"
)

var Logger *slog.Logger

func parseLogLevel(level string) slog.Level {
	switch strings.ToUpper(level) {
	case "DEBUG":
		return slog.LevelDebug
	case "INFO":
		return slog.LevelInfo
	case "WARN", "WARNING":
		return slog.LevelWarn
	case "ERROR":
		return slog.LevelError
	default:
		return slog.LevelError
	}
}

func Init(cfg *config.Config) {
	var handler slog.Handler

	if cfg.Env == "prod" || cfg.Env == "production" {
		handler = slog.NewJSONHandler(os.Stdout, nil)
	} else {
		handler = tint.NewHandler(os.Stdout, &tint.Options{
			Level:      parseLogLevel(cfg.LogLevel),
			TimeFormat: "2006-01-02 15:04:05",
		})
	}

	Logger = slog.New(handler)

	// Optionally: make it global via slog.SetDefault
	slog.SetDefault(Logger)
}
