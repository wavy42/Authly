from fastapi import HTTPException, status


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

bubble_id_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="bubble not found",
)

invalid_document_id = HTTPException(
    status_code=400, detail="Invalid document id"
)
