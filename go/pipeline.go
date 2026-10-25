package main

import (
	"context"
	"fmt"

	"dagger.io/dagger"
)

func main() {
	// Create a shared context
	ctx := context.Background()

	// Run the stages of the pipeline
	if err := Pipeline(ctx); err != nil {
		fmt.Println("Error:", err)
		panic(err)
	}
}

func Pipeline(ctx context.Context) error {
	// Initialize Dagger client
	client, err := dagger.Connect(ctx)
	if err != nil {
		return err
	}
	defer client.Close()

	// The project root is one level above this go/ directory.
	// Only copy what the pipeline needs into the container.
	project := client.Host().Directory("..", dagger.HostDirectoryOpts{
		Include: []string{
			"src",
			"pyproject.toml",
			"uv.lock",
			"README.md",
		},
	})

	pipeline := client.Container().
		// uv image with Python 3.14 (the version required in pyproject.toml)
		From("ghcr.io/astral-sh/uv:python3.14-bookworm").
		WithDirectory("/app", project).
		WithWorkdir("/app").
		// Install dependencies from the lockfile
		WithExec([]string{"uv", "sync"}).
		// Run the pipeline stages in order
		WithExec([]string{"uv", "run", "python", "src/dataset.py"}).
		WithExec([]string{"uv", "run", "python", "src/features.py"}).
		WithExec([]string{"uv", "run", "python", "src/modeling/train.py"}).
		WithExec([]string{"uv", "run", "python", "src/modeling/predict.py"})

	// Copy the pipeline outputs from the container back to the host
	outputs := []string{"data", "models", "reports"}
	for _, dir := range outputs {
		if _, err := pipeline.Directory("/app/" + dir).Export(ctx, "../"+dir); err != nil {
			return err
		}
	}

	fmt.Println("Pipeline finished. Outputs exported to data/, models/ and reports/.")
	return nil
}
