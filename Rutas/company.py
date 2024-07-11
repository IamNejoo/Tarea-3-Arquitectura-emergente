from flask import Blueprint, request, jsonify
from models import db, Company
from schemas import CompanySchema
import uuid

company_bp = Blueprint('company', __name__)
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

@company_bp.route('/api/v1/companies', methods=['POST'])
def create_company():
    try:
        company_name = request.json['company_name']
        company_api_key = str(uuid.uuid4())
        new_company = Company(company_name=company_name, company_api_key=company_api_key)
        db.session.add(new_company)
        db.session.commit()
        print("Company created successfully")
        return company_schema.jsonify(new_company), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@company_bp.route('/api/v1/companies', methods=['GET'])
def get_companies():
    all_companies = Company.query.all()
    result = companies_schema.dump(all_companies)
    return jsonify(result)

