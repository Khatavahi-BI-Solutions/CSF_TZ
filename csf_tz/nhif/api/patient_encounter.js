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
        add_btn_final(frm)
        duplicate(frm)
    },
    refresh: function(frm) {
        set_medical_code(frm)
        duplicate(frm)
    },
    patient_encounter_preliminary_diagnosis: function(frm) {
		set_medical_code(frm)
    },
    patient_encounter_final_diagnosis: function(frm) {
		set_medical_code(frm)
    },

});


frappe.ui.form.on('Codification Table', {
    patient_encounter_preliminary_diagnosis_add: function (frm) {
        set_medical_code(frm)
    },
    patient_encounter_preliminary_diagnosis_remove: function (frm) {
        set_medical_code(frm)
    },
    patient_encounter_final_diagnosis_add: function (frm) {
        set_medical_code(frm)
    },
    patient_encounter_final_diagnosis_remove: function (frm) {
        set_medical_code(frm)
    },
    medical_code(frm, cdt, cdn) {
        set_medical_code(frm)
    }
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
    const final_diagnosis = get_final_diagnosis(frm)
    const preliminary_diagnosis = get_preliminary_diagnosis(frm)
    frappe.meta.get_docfield("Drug Prescription", "medical_code", frm.doc.name).options = final_diagnosis;
    refresh_field("drug_prescription");

    frappe.meta.get_docfield("Lab Prescription", "medical_code", frm.doc.name).options = preliminary_diagnosis
    refresh_field("lab_test_prescription");

    frappe.meta.get_docfield("Procedure Prescription", "medical_code", frm.doc.name).options = final_diagnosis;
    refresh_field("procedure_prescription");

    frappe.meta.get_docfield("Radiology Procedure Prescription", "medical_code", frm.doc.name).options = preliminary_diagnosis;
    refresh_field("radiology_procedure_prescription");

    frappe.meta.get_docfield("Therapy Plan Detail", "medical_code", frm.doc.name).options = final_diagnosis;
    refresh_field("therapies");

    frappe.meta.get_docfield("Diet Recommendation", "medical_code", frm.doc.name).options = final_diagnosis;
    refresh_field("diet_recommendation");

    frm.refresh_fields();
}

var validate_medical_code = function (frm) {
    if (frm.doc.drug_prescription) {
        frm.doc.drug_prescription.forEach(element => {
            if (!get_final_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Drug Prescription' line item ${element.idx}`))
            }
        });
    }
    if (frm.doc.lab_test_prescription) {
        frm.doc.lab_test_prescription.forEach(element => {
            if (!get_preliminary_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Lab Prescription' line item ${element.idx}`))
            }
        });
    }
    if (frm.doc.procedure_prescription) {
        frm.doc.procedure_prescription.forEach(element => {
            if (!get_final_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Procedure Prescription' line item ${element.idx}`))
            }
        });
    }
    if (frm.doc.radiology_procedure_prescription) {
        frm.doc.radiology_procedure_prescription.forEach(element => {
            if (!get_preliminary_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Radiology Procedure Prescription' line item ${element.idx}`))
            }
        });
    }
    if (frm.doc.procedure_prescription) {
        frm.doc.procedure_prescription.forEach(element => {
            if (!get_final_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Therapy Plan Detail' line item ${element.idx}`))
            }
        });
    }
    if (frm.doc.diet_recommendation) {
        frm.doc.diet_recommendation.forEach(element => {
            if (!get_final_diagnosis(frm).includes(element.medical_code)) {
                frappe.throw(__(`The medical code ${element.medical_code} hase been removed but is already used in the order 'Diet Recommendation' line item ${element.idx}`))
            }
        });
    }
}

var add_btn_final = function(frm) {
    if (frm.doc.docstatus==1 && frm.doc.encounter_type != 'Final') {
        frm.add_custom_button(__('Set as Final'), function() {
            frm.set_value("encounter_type", 'Final');
        });
    }
}

var duplicate = function(frm) {
    if (frm.doc.docstatus!=1 || frm.doc.encounter_type == 'Final' || frm.doc.duplicate == 1) {
        return
    }
    frm.add_custom_button(__('Duplicate'), function() {
        frm.save()
        frappe.call({
            method: 'csf_tz.nhif.api.patient_encounter.duplicate_encounter',
            args: {
                'encounter': frm.doc.name
            },
            callback: function (data) {
                if (data.message) {
                    frappe.set_route('Form', 'Patient Encounter', data.message);
                }
            }
        });
    });
}