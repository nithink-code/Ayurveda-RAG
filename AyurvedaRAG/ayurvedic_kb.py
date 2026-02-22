"""
Ayurvedic Knowledge Base
Structured data for populating Qdrant collections.
Each entry has rich metadata for condition-based retrieval.
"""

CONDITIONS = [
    {
        "id": "diabetes_overview",
        "condition": "Diabetes",
        "dosha": "Kapha",
        "type": "condition_overview",
        "text": (
            "Diabetes (Madhumeha) in Ayurveda is classified under Prameha — a group of urinary disorders. "
            "Madhumeha is the most severe form, primarily caused by Kapha dosha aggravation along with vitiation of Vata. "
            "It involves impaired metabolism of glucose, accumulation of ama (metabolic waste), and weakening of ojas (vital energy). "
            "Causes include sedentary lifestyle, excessive intake of sweet, oily, and heavy foods. "
            "Treatment involves Kapha-pacifying diet, herbal formulations, fasting protocols, Panchakarma therapies, and regular exercise."
        )
    },
    {
        "id": "acidity_overview",
        "condition": "Acidity",
        "dosha": "Pitta",
        "type": "condition_overview",
        "text": (
            "Acidity (Amlapitta) is a Pitta disorder in Ayurveda, caused by excessive production of sour (amla) gastric acids. "
            "Triggers include spicy food, irregular eating, stress, alcohol, and suppression of natural urges. "
            "Symptoms include heartburn, sour belching, vomiting, nausea, and discomfort in the chest and stomach. "
            "Ayurvedic management involves cooling and alkaline foods, Pitta-pacifying herbs, lifestyle regularization, "
            "and therapies like Virechana (therapeutic purgation) and Shirodhara for stress-related acidity."
        )
    },
    {
        "id": "thyroid_overview",
        "condition": "Thyroid",
        "dosha": "Vata-Kapha",
        "type": "condition_overview",
        "text": (
            "Thyroid disorders in Ayurveda correlate to 'Galaganda' (goitre) and are linked to Kapha and Vata imbalance. "
            "Hypothyroidism maps to Kapha dominance — sluggishness, weight gain, cold intolerance. "
            "Hyperthyroidism maps to Pitta-Vata — anxiety, weight loss, heat intolerance. "
            "Ayurvedic treatment includes Kanchanar Guggulu, Triphala, specific diet modifications, Nasya therapy, "
            "and yoga practices to stimulate the thyroid gland via the throat chakra (Vishuddha)."
        )
    },
    {
        "id": "anxiety_overview",
        "condition": "Anxiety",
        "dosha": "Vata",
        "type": "condition_overview",
        "text": (
            "Anxiety and stress disorders in Ayurveda are classified as 'Chittodvega' — an aggravation of Vata dosha "
            "in the mind and nervous system. Causes include excessive mental activity, irregular routines, poor sleep, "
            "trauma, and sensory overload. Symptoms include restlessness, fear, palpitations, insomnia, and overthinking. "
            "Ayurvedic treatment focuses on Vata pacification through grounding foods, warm oil massage (Abhyanga), "
            "Shirodhara (oil drip on forehead), Ashwagandha, Brahmi, and establishing a stable daily routine (Dinacharya)."
        )
    },
]

HERBS = [
    # --- Diabetes ---
    {
        "id": "bitter_melon_diabetes",
        "condition": "Diabetes",
        "herb": "Bitter Melon (Karela)",
        "dosha": "Kapha",
        "type": "herb",
        "text": (
            "Bitter Melon (Momordica charantia), known as Karela, is one of the most potent anti-diabetic herbs in Ayurveda. "
            "It contains charantin, vicine, and polypeptide-p — compounds with insulin-like activity that lower blood glucose. "
            "It also improves glucose tolerance and stimulates insulin secretion from the pancreas. "
            "For Madhumeha (diabetes), Karela pacifies Kapha and removes ama from the dhatus (tissues). "
            "Dosage guidance: 50-100 ml fresh juice in the morning or 500 mg extract capsule before meals. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    {
        "id": "fenugreek_diabetes",
        "condition": "Diabetes",
        "herb": "Fenugreek (Methi)",
        "dosha": "Kapha-Vata",
        "type": "herb",
        "text": (
            "Fenugreek (Trigonella foenum-graecum), known as Methi, is a classical Ayurvedic herb for diabetes management. "
            "Its soluble fiber content slows carbohydrate absorption and glucose uptake, reducing post-meal blood sugar spikes. "
            "Fenugreek seeds improve insulin sensitivity and stimulate insulin secretion. "
            "They also lower LDL cholesterol and triglycerides, which are commonly elevated in diabetic patients. "
            "Dosage guidance: Soak 1-2 teaspoons of seeds overnight and consume in the morning, or 500-1000 mg extract. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    {
        "id": "gurmar_diabetes",
        "condition": "Diabetes",
        "herb": "Gurmar (Gymnema)",
        "dosha": "Kapha",
        "type": "herb",
        "text": (
            "Gurmar (Gymnema sylvestre), meaning 'sugar destroyer' in Sanskrit, is a powerful anti-diabetic herb. "
            "It blocks sugar absorption in the intestines, reduces sugar cravings by binding taste receptors, "
            "and stimulates regeneration of pancreatic beta cells responsible for insulin production. "
            "For Ayurvedic Madhumeha treatment, Gurmar is often considered the most specific herb. "
            "Dosage guidance: 200-400 mg standardized extract twice daily before meals. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    # --- Acidity ---
    {
        "id": "licorice_acidity",
        "condition": "Acidity",
        "herb": "Licorice (Yashtimadhu)",
        "dosha": "Pitta-Vata",
        "type": "herb",
        "text": (
            "Licorice root (Glycyrrhiza glabra), known as Yashtimadhu in Ayurveda, is a primary herb for Amlapitta (acidity). "
            "It has powerful demulcent, anti-ulcer, and anti-inflammatory properties. "
            "It forms a protective mucous coating over the stomach lining, reducing irritation from excess acid. "
            "It balances Pitta, soothes the esophagus, and reduces symptoms of GERD and heartburn. "
            "Dosage guidance: 250-500 mg DGL (deglycyrrhizinated licorice) before meals. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    {
        "id": "amalaki_acidity",
        "condition": "Acidity",
        "herb": "Amalaki (Amla)",
        "dosha": "Pitta",
        "type": "herb",
        "text": (
            "Amalaki (Emblica officinalis), commonly known as Indian Gooseberry or Amla, is the best Pitta-pacifying fruit in Ayurveda. "
            "Despite being sour, its post-digestive effect (vipaka) is sweet, making it alkaline-forming in the body. "
            "It reduces stomach acid, heals gastric ulcers, reduces inflammation of the stomach lining, "
            "and is rich in Vitamin C which supports mucosal repair. It is included in Triphala for this reason. "
            "Dosage guidance: 500 mg Amalaki powder or extract, or 20 ml fresh juice twice daily. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    # --- Anxiety ---
    {
        "id": "brahmi_anxiety",
        "condition": "Anxiety",
        "herb": "Brahmi",
        "dosha": "Vata-Pitta",
        "type": "herb",
        "text": (
            "Brahmi (Bacopa monnieri) is the foremost nervine tonic in Ayurveda, specifically indicated for Chittodvega (anxiety). "
            "It calms the nervous system by enhancing GABA activity, reduces cortisol levels, improves cognitive function, "
            "and supports formation of new neural pathways. It is used in Medhya Rasayana (brain-rejuvenating) formulas. "
            "For anxiety, it reduces the racing thoughts and hyperactivity of Vata in the mind. "
            "Dosage guidance: 300-600 mg Bacopa extract daily, or 1 tsp Brahmi powder in warm milk at night. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    {
        "id": "jatamansi_anxiety",
        "condition": "Anxiety",
        "herb": "Jatamansi",
        "dosha": "Vata",
        "type": "herb",
        "text": (
            "Jatamansi (Nardostachys jatamansi) is an Ayurvedic sedative and nervine tonic for anxiety, insomnia, and stress. "
            "It calms Vata in the nervous system, reduces cortisol levels, promotes deep sleep, and balances neurotransmitters "
            "including serotonin and GABA. It is often prescribed alongside Ashwagandha for comprehensive anxiety management. "
            "Jatamansi is particularly effective for anxiety with insomnia and palpitations. "
            "Dosage guidance: 250-500 mg root powder before bedtime with warm milk and honey. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
    # --- Thyroid ---
    {
        "id": "kanchanar_thyroid",
        "condition": "Thyroid",
        "herb": "Kanchanar Guggulu",
        "dosha": "Kapha-Vata",
        "type": "herb",
        "text": (
            "Kanchanar Guggulu is the primary Ayurvedic formulation for thyroid disorders (Galaganda). "
            "Kanchanar (Bauhinia variegata) has specific action on lymphatic and glandular tissue, "
            "reducing swelling and nodules. Combined with Guggulu (a resin), it enhances thyroid metabolism, "
            "reduces Kapha accumulation in the gland, and regulates T3/T4 hormones. "
            "It also has anti-cancer properties and is used for cysts and tumors in Ayurveda. "
            "Dosage guidance: 1-2 tablets twice daily after meals with warm water. "
            "DISCLAIMER: Consult a qualified Ayurvedic practitioner before starting any herbal regimen."
        )
    },
]

DIET_GUIDELINES = [
    {
        "id": "diabetes_diet",
        "condition": "Diabetes",
        "dosha": "Kapha",
        "type": "diet",
        "text": (
            "Ayurvedic Diet Guidelines for Diabetes (Madhumeha):\n"
            "FAVOR: Bitter, astringent, and pungent tastes. Include barley (best grain for diabetes), "
            "old rice (stored for over a year), mung dal, green leafy vegetables, bitter gourd, fenugreek, "
            "turmeric, cinnamon, and amla. Eat warm, light, and easily digestible foods. "
            "Include healthy fats like ghee in small amounts (improves insulin sensitivity).\n"
            "AVOID: Sweet, salty, and sour tastes in excess. Strictly avoid refined sugars, white bread, "
            "processed foods, fruit juices, sweet fruits (banana, mango, grapes), dairy in large quantities, "
            "red meat, and alcohol. Avoid daytime sleeping (causes Kapha aggravation). "
            "Eat smaller, more frequent meals. Never skip breakfast. Monitor portion sizes."
        )
    },
    {
        "id": "acidity_diet",
        "condition": "Acidity",
        "dosha": "Pitta",
        "type": "diet",
        "text": (
            "Ayurvedic Diet Guidelines for Acidity (Amlapitta):\n"
            "FAVOR: Sweet, bitter, and astringent tastes. Include cooling foods like cucumber, "
            "coconut water, pomegranate, sweet grapes, melons, bananas (ripe), milk, ghee, "
            "buttermilk (diluted, room temperature), green vegetables, coriander, fennel, and cardamom. "
            "Eat on a regular schedule. Never skip meals (empty stomach worsens acidity). "
            "Have the largest meal at lunch when digestive fire is strongest.\n"
            "AVOID: Spicy, sour, salty, and pungent foods. Avoid chili, vinegar, fermented foods, "
            "tomatoes (large quantities), citrus fruits (lemon in excess), coffee, tea, alcohol, "
            "carbonated beverages, fried and oily foods. Avoid eating late at night. "
            "Do not lie down immediately after eating. Avoid stress while eating."
        )
    },
    {
        "id": "anxiety_diet",
        "condition": "Anxiety",
        "dosha": "Vata",
        "type": "diet",
        "text": (
            "Ayurvedic Diet Guidelines for Anxiety:\n"
            "FAVOR: Warm, oily, sweet, sour, and salty tastes. Include warm milk with ashwagandha, "
            "ghee, sesame, nuts (almonds soaked overnight), all types of dal, root vegetables, "
            "sweet fruits, and warm spiced foods. Eat regularly at consistent times — this alone "
            "greatly pacifies Vata. Warm herbal teas like chamomile, licorice, and ginger are beneficial.\n"
            "AVOID: Cold, raw, dry, light, and bitter foods. Avoid raw salads, cold smoothies, "
            "caffeine (major Vata aggravator), alcohol, carbonated drinks, frozen foods, "
            "and fasting or irregular eating patterns. Avoid multitasking while eating. "
            "Eat in a calm, nourishing environment."
        )
    },
    {
        "id": "thyroid_diet",
        "condition": "Thyroid",
        "dosha": "Kapha-Vata",
        "type": "diet",
        "text": (
            "Ayurvedic Diet Guidelines for Thyroid Disorders:\n"
            "FAVOR: For hypothyroidism (Kapha type): warm, light, spicy, and dry foods. "
            "Include iodine-rich foods like sea vegetables, black pepper, ginger, turmeric. "
            "For hyperthyroidism (Pitta-Vata type): cooling, grounding foods — ghee, coconut, "
            "sweet fruits, warm milk. In general, Brazil nuts (selenium), pumpkin seeds (zinc), "
            "and leafy greens support thyroid function.\n"
            "AVOID: Goitrogens in raw form (raw broccoli, cabbage, cauliflower, kale) for hypothyroidism "
            "— cooking neutralizes them. Avoid soy products, gluten (for sensitive individuals), "
            "processed foods, and fluoride-containing water. Avoid caffeine for hyperthyroidism."
        )
    },
]

YOGA_PRACTICES = [
    {
        "id": "diabetes_yoga",
        "condition": "Diabetes",
        "dosha": "Kapha",
        "type": "yoga",
        "text": (
            "Yoga Practices for Diabetes (Madhumeha):\n"
            "ASANAS: Dhanurasana (Bow Pose) — massages pancreas and stimulates insulin production. "
            "Ardha Matsyendrasana (Half Spinal Twist) — stimulates pancreas and liver. "
            "Paschimottanasana (Forward Bend) — stretches pancreas. Sarvangasana (Shoulder Stand) — endocrine stimulation. "
            "Viparita Karani (Legs Up Wall) — reduces blood glucose. Warrior poses I and II for building muscle mass.\n"
            "PRANAYAMA: Kapalbhati 15-20 min daily (most important for diabetes) — stimulates pancreatic function. "
            "Anulom Vilom (Alternate Nostril) for overall balance. Bhastrika for metabolism boost.\n"
            "PRACTICE: 45-60 minutes daily in the morning. Walking 30 minutes after meals is highly recommended."
        )
    },
    {
        "id": "acidity_yoga",
        "condition": "Acidity",
        "dosha": "Pitta",
        "type": "yoga",
        "text": (
            "Yoga Practices for Acidity:\n"
            "ASANAS: Vajrasana (Diamond Pose) — uniquely beneficial immediately after meals for digestion. "
            "Ardha Matsyendrasana — massages digestive organs. Pavanmuktasana (Wind Relieving) — reduces gas. "
            "Bitilasana-Marjaryasana (Cat-Cow) — massages abdominal organs. Balasana (Child's Pose) — calms the nervous system. "
            "Bhujangasana (Cobra) — opens chest and stimulates digestive fire mildly.\n"
            "PRANAYAMA: Sheetali (Cooling Breath) — most important for Pitta/acidity conditions. "
            "Shitkari (Hissing Breath) — cools the body. Nadi Shodhana for overall balance. "
            "AVOID: Kapalbhati and intense Bhastrika as they heat the body and worsen Pitta.\n"
            "PRACTICE: 30 minutes daily. Practice in the morning on an empty stomach."
        )
    },
    {
        "id": "anxiety_yoga",
        "condition": "Anxiety",
        "dosha": "Vata",
        "type": "yoga",
        "text": (
            "Yoga Practices for Anxiety:\n"
            "ASANAS: Balasana (Child's Pose) — deeply grounding and calming. "
            "Viparita Karani (Legs Up Wall) — activates parasympathetic nervous system. "
            "Savasana (Corpse Pose) — deep relaxation, practice extended for 15-20 min. "
            "Uttanasana (Standing Forward Bend) — calms Vata in the head. "
            "Setu Bandhasana (Bridge Pose) — opens heart center. Gentle Surya Namaskar (Sun Salutation) — 3-5 rounds.\n"
            "PRANAYAMA: Nadi Shodhana (Alternate Nostril) — 15 min daily, most effective for Vata anxiety. "
            "Bhramari (Humming Bee) — calms nervous system immediately. "
            "4-7-8 breathing technique for acute anxiety episodes.\n"
            "PRACTICE: Daily, gentle, slow-paced yoga. Yin yoga and restorative yoga are ideal."
        )
    },
    {
        "id": "thyroid_yoga",
        "condition": "Thyroid",
        "dosha": "Kapha-Vata",
        "type": "yoga",
        "text": (
            "Yoga Practices for Thyroid Disorders:\n"
            "ASANAS: Sarvangasana (Shoulder Stand) — the most important pose; directly stimulates thyroid. "
            "Halasana (Plow Pose) — stimulates thyroid and parathyroid glands. "
            "Matsyasana (Fish Pose) — stretches the throat area stimulating the gland. "
            "Setu Bandhasana (Bridge) — gentle thyroid stimulation. "
            "Bhujangasana (Cobra) — opens throat and chest. Ustrasana (Camel Pose) — throat stretch.\n"
            "PRANAYAMA: Ujjayi (Ocean Breath) — specifically activates the throat area and Vishuddha chakra. "
            "Bhramari for stress-related thyroid dysfunction. Kapalbhati for hypothyroidism.\n"
            "PRACTICE: 45 minutes daily. Consult practitioner before inversions if you have hyperthyroidism."
        )
    },
]

PRECAUTIONS = [
    {
        "id": "diabetes_precautions",
        "condition": "Diabetes",
        "dosha": "Kapha",
        "type": "precautions",
        "text": (
            "Precautions & When to See a Doctor for Diabetes:\n"
            "⚠️ WHEN TO CONSULT A DOCTOR IMMEDIATELY:\n"
            "• Blood sugar extremely high (>300 mg/dL) or low (<70 mg/dL)\n"
            "• Signs of diabetic ketoacidosis: vomiting, confusion, fruity-smelling breath\n"
            "• Foot wounds that don't heal, numbness, or color changes in feet\n"
            "• Vision problems or sudden vision loss\n"
            "• Chest pain or shortness of breath\n\n"
            "⚠️ AYURVEDIC TREATMENT PRECAUTIONS:\n"
            "• Never stop insulin or diabetes medications without doctor supervision\n"
            "• Herbs like Gurmar and Bitter Melon have hypoglycemic effects — monitor glucose\n"
            "• Fasting should only be done under medical supervision for diabetics\n"
            "• Regular blood glucose monitoring is essential during herbal treatment\n"
            "• DISCLAIMER: This plan is for wellness guidance only, not a substitute for medical care."
        )
    },
    {
        "id": "acidity_precautions",
        "condition": "Acidity",
        "dosha": "Pitta",
        "type": "precautions",
        "text": (
            "Precautions & When to See a Doctor for Acidity:\n"
            "⚠️ WHEN TO CONSULT A DOCTOR IMMEDIATELY:\n"
            "• Difficulty swallowing or food getting stuck\n"
            "• Blood in vomit or dark/tarry stools (sign of bleeding ulcer)\n"
            "• Unexplained and persistent weight loss\n"
            "• Severe, crushing chest pain (rule out heart conditions)\n"
            "• Persistent symptoms despite treatment (possible Barrett's esophagus)\n\n"
            "⚠️ AYURVEDIC TREATMENT PRECAUTIONS:\n"
            "• Do not take Triphala if you have severe active gastritis\n"
            "• Licorice root with glycyrrhizin (non-DGL) can raise blood pressure\n"
            "• If on antacids, consult before adding herbal supplements\n"
            "• Avoid self-medicating for more than 2 weeks without reassessment\n"
            "• DISCLAIMER: This plan is for wellness guidance only, not a substitute for medical care."
        )
    },
    {
        "id": "anxiety_precautions",
        "condition": "Anxiety",
        "dosha": "Vata",
        "type": "precautions",
        "text": (
            "Precautions & When to See a Doctor for Anxiety:\n"
            "⚠️ WHEN TO CONSULT A DOCTOR IMMEDIATELY:\n"
            "• Panic attacks with chest pain and difficulty breathing\n"
            "• Thoughts of self-harm or suicide — seek emergency help immediately\n"
            "• Severe agoraphobia preventing daily functioning\n"
            "• Anxiety accompanied by psychosis or paranoia\n"
            "• Complete inability to sleep for multiple nights\n\n"
            "⚠️ AYURVEDIC TREATMENT PRECAUTIONS:\n"
            "• Do not stop anti-anxiety medications abruptly — taper under doctor guidance\n"
            "• Ashwagandha and Jatamansi may interact with sedatives\n"
            "• Brahmi should be used cautiously in hypothyroidism patients\n"
            "• Intense pranayama like Kapalbhati can worsen anxiety — use gentle techniques\n"
            "• DISCLAIMER: This plan is for wellness guidance only, not a substitute for medical care."
        )
    },
    {
        "id": "thyroid_precautions",
        "condition": "Thyroid",
        "dosha": "Kapha-Vata",
        "type": "precautions",
        "text": (
            "Precautions & When to See a Doctor for Thyroid Disorders:\n"
            "⚠️ WHEN TO CONSULT A DOCTOR IMMEDIATELY:\n"
            "• Thyroid storm (rapid heartbeat, fever, confusion) — medical emergency\n"
            "• Myxedema coma signs (extreme cold intolerance, drowsiness, slow heartbeat)\n"
            "• Rapidly growing thyroid nodule or goitre\n"
            "• Difficulty breathing or swallowing due to enlarged gland\n"
            "• Significant changes in heart rhythm\n\n"
            "⚠️ AYURVEDIC TREATMENT PRECAUTIONS:\n"
            "• Never stop thyroid medication (levothyroxine) without endocrinologist approval\n"
            "• Kanchanar Guggulu timing must be separated from thyroid medications by 4 hours\n"
            "• Excess iodine from sea vegetables can worsen hyperthyroidism\n"
            "• Sarvangasana (shoulder stand) should be avoided in hyperthyroidism\n"
            "• Monitor TSH, T3, T4 levels regularly during Ayurvedic treatment\n"
            "• DISCLAIMER: This plan is for wellness guidance only, not a substitute for medical care."
        )
    },
]

LIFESTYLE_ADVICE = [
    {
        "id": "diabetes_lifestyle",
        "condition": "Diabetes",
        "dosha": "Kapha",
        "type": "lifestyle",
        "text": (
            "Lifestyle Advice for Diabetes (Dinacharya):\n"
            "🌅 MORNING ROUTINE: Wake by 5-6 AM. Drink warm water. Walk 30-45 minutes briskly. "
            "Practice Kapalbhati pranayama for 15-20 min. Eat breakfast at consistent time.\n"
            "☀️ DAY: Monitor blood glucose before and after meals. Avoid sedentary behavior — "
            "take 10-15 min walk after each meal. Stay hydrated with water and herbal teas. "
            "Manage stress — it directly impacts blood sugar. Limit screen and sitting time.\n"
            "🌙 EVENING: Dinner by 6:30-7 PM. Take herbs as directed. Foot care — check for wounds, "
            "apply warm sesame oil to feet. Sleep by 10 PM — poor sleep raises blood sugar.\n"
            "💡 KEY: Consistent mealtimes, exercise, and sleep are as important as diet for diabetes. "
            "Stress management through meditation reduces cortisol which directly raises blood sugar."
        )
    },
    {
        "id": "acidity_lifestyle",
        "condition": "Acidity",
        "dosha": "Pitta",
        "type": "lifestyle",
        "text": (
            "Lifestyle Advice for Acidity (Dinacharya):\n"
            "🌅 MORNING ROUTINE: Wake by 6-7 AM (Pitta constitution can sleep slightly later than Kapha). "
            "Drink room-temperature or slightly warm water — NOT iced. Avoid coffee on empty stomach. "
            "10-15 min gentle yoga. Eat a calm, relaxed breakfast — never rush meals.\n"
            "☀️ DAY: Largest meal at lunch (12-2 PM) when digestive fire is strongest. "
            "Sit quietly after meals for 10-15 minutes. Sit in Vajrasana after lunch for 5-10 min. "
            "Avoid intense exercise on a full stomach. Do not eat at the desk while working.\n"
            "🌙 EVENING: Light dinner before 7 PM. Walk 15-20 min after dinner (not vigorous). "
            "Elevate head of bed 6-8 inches if you have night reflux. No eating 3 hours before bed.\n"
            "💡 KEY: Emotional stress is the greatest Pitta aggravator. Meditation, spending time in nature, "
            "moon-gazing, and cooling activities are powerful therapeutic tools."
        )
    },
    {
        "id": "anxiety_lifestyle",
        "condition": "Anxiety",
        "dosha": "Vata",
        "type": "lifestyle",
        "text": (
            "Lifestyle Advice for Anxiety (Dinacharya — the most important prescription for Vata):\n"
            "🌅 MORNING ROUTINE: Wake at the SAME time every day — consistency is medicine for Vata. "
            "Warm oil self-massage (Abhyanga) with sesame oil for 15-20 min before bath. "
            "Gentle yoga. Warm, nourishing breakfast — NEVER skip breakfast for anxiety.\n"
            "☀️ DAY: Meals at consistent times. Avoid skipping meals. Limit digital stimulation — "
            "limit social media. Take breaks from work. Walk in nature. Limit decision-making when anxious.\n"
            "🌙 EVENING: Dinner by 7 PM. Warm milk with Ashwagandha and nutmeg before bed. "
            "Apply warm oil to feet and scalp. Journal. Sleep by 10 PM. "
            "Maintain dark, quiet bedroom. SAME sleep time daily is crucial.\n"
            "💡 KEY: ROUTINE is the #1 treatment for Vata anxiety. Every single daily activity at a fixed time "
            "sends a signal of safety to the nervous system and dramatically reduces anxiety."
        )
    },
]

# All data combined for easy access
ALL_KNOWLEDGE = {
    "conditions": CONDITIONS,
    "herbs": HERBS,
    "diet_guidelines": DIET_GUIDELINES,
    "yoga_practices": YOGA_PRACTICES,
    "precautions": PRECAUTIONS,
    "lifestyle": LIFESTYLE_ADVICE,
}

# Supported conditions mapping
SUPPORTED_CONDITIONS = {
    "Diabetes": ["Kapha", "high blood sugar, Madhumeha, insulin resistance"],
    "Acidity": ["Pitta", "heartburn, GERD, Amlapitta, gastritis"],
    "Thyroid": ["Kapha-Vata", "hypothyroidism, hyperthyroidism, Galaganda"],
    "Anxiety": ["Vata", "stress, panic, insomnia, Chittodvega"],
}
