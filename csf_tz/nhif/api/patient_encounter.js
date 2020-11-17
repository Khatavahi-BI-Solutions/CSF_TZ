frappe.ui.form.on('Patient Encounter', {
    on_submit: function (frm) {
        if (!frm.doc.patient_encounter_final_diagnosis) {
            frappe.throw(__("Final diagnosis mandatory before submit"))
        }
    },
    validate: function (frm) {
        validate_medical_code(frm)
    },
    onload: function (frm) {
        set_medical_code(frm)
    },
    refresh: function(frm) {
		set_medical_code(frm)
    },
    patient_encounter_preliminary_diagnosis: function(frm) {
		set_medical_code(frm)
    },
    patient_encounter_final_diagnosis: function(frm) {
		set_medical_code(frm)
    },

});

var get_preliminary_diagnosis = function (frm){
    const diagnosis_list = [];
    frm.doc.patient_encounter_preliminary_diagnosis.forEach(element => {
        diagnosis_list.push(element.medical_code)
    });
    return diagnosis_list
}

var get_final_diagnosis = function (frm){
    const diagnosis_list = [];
    frm.doc.patient_encounter_final_diagnosis.forEach(element => {
        diagnosis_list.push(element.medical_code)
    });
    return diagnosis_list
}

var set_medical_code = function (frm) {
    frappe.meta.get_docfield("Drug Prescription", "medical_code", frm.doc.name).options = get_final_diagnosis(frm);
    refresh_field("patient_encounter_preliminary_diagnosis");

    frappe.meta.get_docfield("Lab Prescription", "medical_code", frm.doc.name).options = get_preliminary_diagnosis(frm);
    refresh_field("lab_test_prescription");

    frappe.meta.get_docfield("Procedure Prescription", "medical_code", frm.doc.name).options = get_final_diagnosis(frm);
    refresh_field("procedure_prescription");

    frappe.meta.get_docfield("Radiology Procedure Prescription", "medical_code", frm.doc.name).options = get_preliminary_diagnosis(frm);
    refresh_field("radiology_procedure_prescription");

    frappe.meta.get_docfield("Therapy Plan Detail", "medical_code", frm.doc.name).options = get_final_diagnosis(frm);
    refresh_field("therapies");

    frappe.meta.get_docfield("Diet Recommendation", "medical_code", frm.doc.name).options = get_final_diagnosis(frm);
    refresh_field("diet_recommendation");

    frm.refresh_fields();
}

var validate_medical_code = function (frm) {
    frm.doc.patient_encounter_preliminary_diagnosis.forEach(element => {
        if (!get_final_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Drug Prescription' line item ${element.idx}`))
        }
    });
    frm.doc.lab_test_prescription.forEach(element => {
        if (!get_preliminary_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Lab Prescription' line item ${element.idx}`))
        }
    });
    frm.doc.procedure_prescription.forEach(element => {
        if (!get_final_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Procedure Prescription' line item ${element.idx}`))
        }
    });
    frm.doc.radiology_procedure_prescription.forEach(element => {
        if (!get_preliminary_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Radiology Procedure Prescription' line item ${element.idx}`))
        }
    });
    frm.doc.therapies.forEach(element => {
        if (!get_final_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Therapy Plan Detail' line item ${element.idx}`))
        }
    });
    frm.doc.diet_recommendation.forEach(element => {
        if (!get_final_diagnosis(frm).includes(element.medical_code)) {
            frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Diet Recommendation' line item ${element.idx}`))
        }
    });
}