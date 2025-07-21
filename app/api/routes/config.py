# # app/routers/config.py

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

# router = APIRouter(prefix="/config", tags=["Config"])


# # --- YEARS ---
# @router.post("/years/")
# def add_year(
#     year: schemas.YearCreate,
#     db: Session = Depends(auth.get_db),
#     current_user: models.User = Depends(auth.get_current_user),
# ):
#     if current_user.role != models.RoleEnum.admin:
#         raise HTTPException(status_code=403, detail="Only admins can add years")
#     return crud.create_year(db, year)


# @router.get("/years/")
# def list_years(db: Session = Depends(auth.get_db)):
#     return crud.get_years(db)
