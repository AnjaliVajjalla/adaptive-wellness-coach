# Feedback Interpretation Evaluation Baseline

Date: September 10, 2026

Model: gpt-5-mini

## Scope

The dataset contains 20 fictional workout-feedback cases. It evaluates:

- Difficulty classification
- Missed workout days
- Disliked exercise identifiers
- Requested workout focus
- Possible need for safety rescreening

No personal health or workout data is included.

## Method

The local evaluation runner sends each fictional feedback statement to the
structured feedback interpreter. A deterministic grader compares the returned
Pydantic object with the expected answer. List contents are compared without
requiring the same order.

## Measured Results

The first 12 clear cases passed 12 of 12.

After adding eight harder cases, the 20-case run produced:

- Whole-case accuracy: 19 of 20, or 95%
- Difficulty accuracy: 19 of 20, or 95%
- Missed-days accuracy: 20 of 20, or 100%
- Disliked-exercises accuracy: 20 of 20, or 100%
- Requested-focus accuracy: 20 of 20, or 100%
- Safety-rescreening accuracy: 20 of 20, or 100%

## Failure Analysis and Correction

The failed case used the phrase “Bodyweight squats were fine.” The expected
difficulty was not_stated, while the model reasonably interpreted “fine” as
appropriate. This made the reference label ambiguous.

The wording was changed to “I did not dislike bodyweight squats,” which tests
the intended exercise-preference contrast without implying difficulty. A
targeted one-case live retest then passed every field.

The corrected result is based on the original 19 passing cases plus the
targeted retest. It is not presented as a second single-run 20-of-20 result.

## Automated Verification

Six evaluation-system tests pass, and the complete project suite contains 179
passing tests in Docker. Automated tests use fake AI responses and cannot make
paid API calls.

## Limitations

- The evaluation dataset is small and synthetic.
- Most cases use concise English feedback.
- The results come from one model configuration and limited live runs.
- Model behavior may vary across repeated runs.
- Plan-explanation quality does not yet have an aggregate scored dataset.
