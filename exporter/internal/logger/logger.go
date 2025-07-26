package logger

import (
	"log/slog"
	"os"

	"github.com/lmittmann/tint"
)

var Logger *slog.Logger

func Init(env string) {
	var handler slog.Handler

	if env == "prod" {
		handler = slog.NewJSONHandler(os.Stdout, nil)
	} else {
		handler = tint.NewHandler(os.Stdout, &tint.Options{
			Level:      slog.LevelDebug,
			TimeFormat: "15:04:05",
		})
	}

	Logger = slog.New(handler)

	// Optionally: make it global via slog.SetDefault
	slog.SetDefault(Logger)
}
