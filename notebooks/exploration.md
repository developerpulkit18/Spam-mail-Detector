# Exploration Notes

## Dataset: SMS Spam Collection

The SMS Spam Collection dataset contains 5,574 SMS messages in English,
tagged as either **ham** (legitimate) or **spam**.

### Key Observations

- **Class imbalance**: ~87% ham vs ~13% spam
- **Spam characteristics**: Often contains UPPERCASE, URLs, phone numbers, 
  money references, urgency words (URGENT, FREE, WINNER, CONGRATULATIONS)
- **Ham characteristics**: Conversational tone, shorter messages, 
  personal references

### Feature Engineering Decisions

1. **TF-IDF** chosen over Bag of Words for better term weighting
2. **Bigrams** included (ngram_range=(1,2)) to capture phrases like "free entry"
3. **Sublinear TF** enabled to dampen the effect of very frequent terms
4. **Max features** set to 5000 to balance dimensionality vs information

### Model Selection Rationale

| Model | Why Selected |
|-------|-------------|
| Multinomial NB | Classical text classification baseline, fast, works well with sparse features |
| Logistic Regression | Strong linear classifier, good interpretability |
| SVM (Linear) | Excellent for high-dimensional sparse data |
| Random Forest | Non-linear ensemble, good for capturing complex patterns |
