from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="unsloth/DeepSeek-R1-GGUF",
    local_dir="DeepSeek-R1-GGUF",
    allow_patterns=["*UD-IQ1_S*"]
)
