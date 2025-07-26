package config

import (
	"log/slog"

	"github.com/caarlos0/env/v11"
	"github.com/joho/godotenv"
)

type Config struct {
	Env      string `env:"ENV" envDefault:"dev"`
	Debug    bool   `env:"DEBUG" debug:"true"`
	LogLevel string `env:"LOG_LEVEL" envDefault:"info"`
}

func New(envFile string) (*Config, error) {
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
