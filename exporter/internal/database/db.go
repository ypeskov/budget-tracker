package database

import (
	"fmt"
	"log/slog"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/jmoiron/sqlx"

	"orgfin.run/exporter/internal/config"
)

var DbInstance *Database

type Database struct {
	Db    *sqlx.DB
	DbUrl string
}

func New(cfg *config.Config) (*Database, error) {
	if DbInstance != nil {
		slog.Info("Returning existing database instance")
		return DbInstance, nil
	}

	DbInstance = &Database{
		DbUrl: fmt.Sprintf(
			"postgres://%s:%s@%s:%s/%s?sslmode=disable",
			cfg.DBUser, cfg.DBPassword, cfg.DBHost, cfg.DBPort, cfg.DBName,
		),
	}

	db, err := sqlx.Connect("pgx", DbInstance.DbUrl)
	if err != nil {
		slog.Error("Failed to connect to database", "error", err)
		return nil, err
	}
	slog.Info("Connected to database", "database", cfg.DBName)

	DbInstance.Db = db

	return DbInstance, nil
}
