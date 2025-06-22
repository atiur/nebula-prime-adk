
ENDPOIINT='<Your API endpoint>'
curl -XPOST $ENDPOIINT -H "Content-Type: application/json" -d '{
    "user_id": "u_1",
    "state": {
        "clinical_context": "nephrology",
        "clinical_reports": "Patient Name: John Doe\n Date of Birth: June 4, 1995\n Age: 30 years\n Study Date: June 5, 2025\n Referring Physician: Dr. Jane Smith \nProcedure: Non-Contrast CT Scan of the Abdomen and Pelvis  \n Indication: Acute right flank pain with suspected nephrolithiasis.  \nFindings: Kidneys: The right kidney exhibits mild hydronephrosis with perinephric fat stranding. A 6 mm hyperdense calculus is identified at the right ureteropelvic junction (UPJ), consistent with a nephrolithiasis. The left kidney appears normal with no evidence of calculi or hydronephrosis.\n Ureters: The right proximal ureter is dilated up to the level of the obs \ntructing calculus. No additional stones are visualized along the course of the ureters.\n Bladder: Normal in appearance with no intraluminal calculi. Other Findings: No evidence of appendicitis, diverticulitis, or other intra-abdominal pathology.\n Impression:6 mm obstructing calculus at the right ureteropelvic junction causing mild hydronephrosis and perinephric fat stranding, indicative of acute nephrolithiasis. No additional urinary tract calculi identified. Recommendations: Urological consultation for management of obstructing ureteral stone. Consideration of pain management and hydration therapy. Follow-up imaging to monitor for stone passage or need for intervention.\n Radiologist: Dr. Emily Johnson, MD."
    }
}'