import asyncio

from auth.domain.models.address import Address
from auth.domain.models.company import Company
from auth.domain.models.user import User
from auth.infra.infra import Infra
from auth.infra.sqlalchemy.address import SaAddress
from auth.infra.sqlalchemy.company import SaCompany
from auth.infra.sqlalchemy.user import SaUser
from core.models.money import Money
from infra.sqlalchemy.db import create_tables
from infra.sqlalchemy.db import init_rdb


async def main():
    init_rdb(url="sqlite+aiosqlite:///:memory:", debug=True)
    await create_tables(tables=[
        SaCompany, 
        SaUser, 
        SaAddress,
    ])

    company = Company(
        id=1, 
        name="株式会社ABC", 
        fund=Money(amount="100", currency="JPY"),
    )

    person_a = User(id=1, name="AAAA", company_id=company.id)
    company.add_employee(person_a)

    person_b = User(id=2, name="BBBB", company_id=company.id)
    company.add_employee(person_b)

    address = Address(id=1, postal_code="123-4567", user_id=person_a.id)
    person_a.add_address(address)


    external = Infra()
    sa_tx_manager = external.get_sa_transaction_manager()
    tx_manager = external.get_transaction_manager([sa_tx_manager])
    company_repository = external.get_company_repository()

    async with tx_manager.start_transaction():
        await company_repository.create(company)
    # await company_repository.create(company)

    company.name = "株式会社ABC改"
    await company_repository.update(company)

    result = await company_repository.list_companies()
    for company in result:
        print(
            f"Company ({company.id}): {company.name} {company.fund} {company.some_hidden_field}"
        )
        for employee in company.employees:
            print(f"    Employee: {employee.id} {employee.name} {employee}")
            for address in employee.addresses:
                print(f"        Address: {address.id} {address.postal_code}")


asyncio.run(main())
