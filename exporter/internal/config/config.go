package config

import (
	"log/slog"

	"github.com/caarlos0/env/v11"
	"github.com/joho/godotenv"
)

type Config struct {
	Env        string `env:"ENV" envDefault:"dev"`
	Debug      bool   `env:"DEBUG" debug:"true"`
	LogLevel   string `env:"LOG_LEVEL" envDefault:"info"`
	DBUser     string `env:"DB_USER" envDefault:"postgres"`
	DBPassword string `env:"DB_PASSWORD" envDefault:"123"`
	DBHost     string `env:"DB_HOST" envDefault:"localhost"`
	DBName     string `env:"DB_NAME" envDefault:"db-orgfin"`
	DBPort     string `env:"DB_PORT" envDefault:"5432"`
}

func New(envFile string) (*Config, error) {
	slog.Info("Loading .env file", "file", envFile)
	if err := godotenv.Load(envFile); err != nil {
		slog.Warn("Failed to load .env file", "error", err)
	}

	var cfg Config
	if err := env.Parse(&cfg); err != nil {
		slog.Error("Failed to parse config", "error", err)
		return nil, err
	}
	return &cfg, nil
}
