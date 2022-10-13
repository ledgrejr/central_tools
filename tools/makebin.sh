 
# macos
GOOS=darwin GOARCH=amd64 go build -o bin/$1-macos $1.go

# windows 
GOOS=windows GOARCH=amd64 go build -o bin/$1.exe $1.go

# linux 
GOOS=linux GOARCH=amd64 go build -o bin/$1-linux $1.go
