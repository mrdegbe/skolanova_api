from app.core.database import SessionLocal
from app.models.tenant import Tenant

def seed_tenants():
    db = SessionLocal()

    tenants = [
        Tenant(
            name="Sunshine International School",
            slug="sunshine",
            school_logo="https://yourcdn.com/logos/sunshine.png"
        ),
        Tenant(
            name="Future Stars Academy",
            slug="futurestars",
            school_logo="https://yourcdn.com/logos/futurestars.png"
        )
    ]

    for tenant in tenants:
        existing = db.query(Tenant).filter(Tenant.slug == tenant.slug).first()
        if not existing:
            db.add(tenant)

    db.commit()
    db.close()
    print("✅ Sample tenants added!")

if __name__ == "__main__":
    seed_tenants()
