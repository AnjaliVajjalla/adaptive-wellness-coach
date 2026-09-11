const form = document.querySelector("#plan-form");
const formMessage = document.querySelector("#form-message");
const formSteps = [...document.querySelectorAll(".form-step")];
const progressSteps = [...document.querySelectorAll(".progress-step")];
const generateButton = document.querySelector("#generate-button");
const planResult = document.querySelector("#plan-result");
const resultContent = document.querySelector("#result-content");

const requiredGroups = {
  1: [
    "available_workout_days",
    "available_equipment",
    "preferred_activities",
    "disliked_activities",
    "preferred_intensity",
  ],
  2: [
    "pregnant_or_postpartum",
    "current_injury_or_rehabilitation",
    "eating_disorder_concern",
    "complex_or_uncontrolled_medical_condition",
    "requests_diagnosis_or_treatment",
    "extreme_weight_loss_goal",
    "requests_medication_supplement_or_therapeutic_diet",
  ],
};

let currentStep = 1;
const profileId = `profile_${Date.now().toString(36)}`;

function selectedValues(name) {
  return [...form.querySelectorAll(`[name="${name}"]:checked`)].map(
    (input) => input.value,
  );
}

function selectedBoolean(name) {
  return form.querySelector(`[name="${name}"]:checked`)?.value === "true";
}

function syncAdditionalGoals() {
  const primaryGoal = form.elements.primary_goal.value;
  const additionalGoalInputs = form.querySelectorAll(
    '[name="additional_goals"]',
  );

  additionalGoalInputs.forEach((input) => {
    const duplicatesPrimaryGoal = input.value === primaryGoal;
    input.disabled = duplicatesPrimaryGoal;
    input.closest("label").classList.toggle(
      "is-disabled",
      duplicatesPrimaryGoal,
    );

    if (duplicatesPrimaryGoal) {
      input.checked = false;
    }
  });
}

function buildPlanRequest() {
  return {
    profile: {
      profile_id: profileId,
      primary_goal: form.elements.primary_goal.value,
      additional_goals: selectedValues("additional_goals"),
      experience_level: form.elements.experience_level.value,
      current_activity_level: form.elements.current_activity_level.value,
      available_workout_days: selectedValues("available_workout_days"),
      session_duration: Number(form.elements.session_duration.value),
      available_equipment: selectedValues("available_equipment"),
      preferred_activities: selectedValues("preferred_activities"),
      disliked_activities: selectedValues("disliked_activities"),
      preferred_intensity: selectedValues("preferred_intensity")[0],
    },
    safety_answers: {
      pregnant_or_postpartum: selectedBoolean("pregnant_or_postpartum"),
      current_injury_or_rehabilitation: selectedBoolean(
        "current_injury_or_rehabilitation",
      ),
      eating_disorder_concern: selectedBoolean("eating_disorder_concern"),
      complex_or_uncontrolled_medical_condition: selectedBoolean(
        "complex_or_uncontrolled_medical_condition",
      ),
      requests_diagnosis_or_treatment: selectedBoolean(
        "requests_diagnosis_or_treatment",
      ),
      extreme_weight_loss_goal: selectedBoolean("extreme_weight_loss_goal"),
      requests_medication_supplement_or_therapeutic_diet: selectedBoolean(
        "requests_medication_supplement_or_therapeutic_diet",
      ),
    },
    challenging_intensity_confirmed:
      form.elements.challenging_intensity_confirmed.checked,
  };
}

function addReviewSection(container, heading, rows) {
  const section = document.createElement("section");
  const title = document.createElement("h3");
  const list = document.createElement("dl");

  title.textContent = heading;
  section.className = "review-section";
  section.append(title, list);

  rows.forEach(([label, value]) => {
    const term = document.createElement("dt");
    const description = document.createElement("dd");
    term.textContent = label;
    description.textContent = value || "None selected";
    list.append(term, description);
  });

  container.append(section);
}

function renderReview() {
  const request = buildPlanRequest();
  const profile = request.profile;
  const summary = document.querySelector("#review-summary");
  const confirmation = document.querySelector("#intensity-confirmation");
  const needsConfirmation =
    profile.preferred_intensity === "Challenging" &&
    (profile.experience_level === "Complete beginner" ||
      profile.current_activity_level === "Sedentary");

  summary.replaceChildren();
  addReviewSection(summary, "Plan preferences", [
    ["Primary goal", profile.primary_goal],
    ["Additional goals", profile.additional_goals.join(", ")],
    ["Experience", profile.experience_level],
    ["Activity level", profile.current_activity_level],
    ["Session duration", `${profile.session_duration} minutes`],
    ["Available days", profile.available_workout_days.join(", ")],
  ]);
  addReviewSection(summary, "Activities and equipment", [
    ["Equipment", profile.available_equipment.join(", ")],
    ["Preferred activities", profile.preferred_activities.join(", ")],
    ["Disliked activities", profile.disliked_activities.join(", ")],
    ["Intensity", profile.preferred_intensity],
  ]);
  addReviewSection(summary, "Safety check", [
    [
      "Result preview",
      Object.values(request.safety_answers).some(Boolean)
        ? "One or more answers require the planner to stop"
        : "All answers are within the planner's scope",
    ],
  ]);

  confirmation.hidden = !needsConfirmation;
  if (!needsConfirmation) {
    form.elements.challenging_intensity_confirmed.checked = false;
  }
}

function clearMessage() {
  formMessage.hidden = true;
  formMessage.textContent = "";
  formMessage.dataset.tone = "";
}

function showMessage(message, tone = "error") {
  formMessage.textContent = message;
  formMessage.dataset.tone = tone;
  formMessage.hidden = false;
  formMessage.focus();
}

function createTextElement(tagName, text, className = "") {
  const element = document.createElement(tagName);
  element.textContent = text;
  if (className) {
    element.className = className;
  }
  return element;
}

function formatFocus(focus) {
  return focus.replaceAll("_", " ").replace(/\b\w/g, (letter) =>
    letter.toUpperCase(),
  );
}

function formatPrescription(exercise) {
  if (exercise.prescription_type === "sets_reps") {
    return `${exercise.sets} sets of ${exercise.repetitions_min}-${exercise.repetitions_max} reps`;
  }
  return `${exercise.minutes} minutes`;
}

function renderGeneratedPlan(result) {
  const heading = createTextElement("h2", "Your weekly plan");
  heading.id = "result-heading";
  heading.tabIndex = -1;
  const summary = createTextElement("p", result.weekly_summary, "result-summary");
  const totals = document.createElement("div");
  const days = document.createElement("div");

  totals.className = "totals-grid";
  [
    ["Workout days", result.totals.workout_days],
    ["Planned minutes", result.totals.total_planned_minutes],
    ["Strength", result.totals.strength_sessions],
    ["Cardio", result.totals.cardio_sessions],
    ["Mobility", result.totals.mobility_sessions],
  ].forEach(([label, value]) => {
    const item = document.createElement("div");
    item.append(
      createTextElement("strong", String(value)),
      createTextElement("span", label),
    );
    totals.append(item);
  });

  days.className = "plan-days";
  result.days.forEach((day) => {
    const card = document.createElement("article");
    const cardHeader = document.createElement("div");
    const badge = createTextElement(
      "span",
      day.day_type === "rest" ? "Rest" : `${day.total_minutes} min`,
      `day-badge ${day.day_type}`,
    );

    card.className = "day-card";
    cardHeader.className = "day-card-header";
    cardHeader.append(
      createTextElement("h3", day.day),
      badge,
    );
    card.append(
      cardHeader,
      createTextElement("p", formatFocus(day.focus), "day-focus"),
      createTextElement("p", day.explanation, "day-explanation"),
    );

    if (day.exercises.length) {
      const exerciseList = document.createElement("ul");
      exerciseList.className = "exercise-list";
      day.exercises.forEach((exercise) => {
        const item = document.createElement("li");
        item.append(
          createTextElement("strong", exercise.name),
          createTextElement("span", formatPrescription(exercise)),
        );
        exerciseList.append(item);
      });
      card.append(exerciseList);
    }

    days.append(card);
  });

  resultContent.replaceChildren(heading, summary, totals, days);
  planResult.hidden = false;
  heading.focus();
  planResult.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderStoppedResult(result) {
  const headingText =
    result.status === "blocked" ? "A plan was not generated" : "Confirmation required";
  const heading = createTextElement("h2", headingText);
  heading.id = "result-heading";
  heading.tabIndex = -1;

  resultContent.replaceChildren(
    heading,
    createTextElement("p", result.message, "result-summary"),
  );
  planResult.hidden = false;
  heading.focus();
  planResult.scrollIntoView({ behavior: "smooth", block: "start" });
}

function validationMessage(detail) {
  if (!Array.isArray(detail) || !detail.length) {
    return "The request was not accepted. Review the form and try again.";
  }
  const firstError = detail[0];
  const field = firstError.loc?.slice(1).join(" → ");
  return `${field || "Request"}: ${firstError.msg}`;
}

function showStep(stepNumber) {
  currentStep = stepNumber;
  clearMessage();

  formSteps.forEach((step) => {
    step.hidden = Number(step.dataset.step) !== stepNumber;
  });

  progressSteps.forEach((step, index) => {
    const isActive = index + 1 === stepNumber;
    step.classList.toggle("is-active", isActive);
    if (isActive) {
      step.setAttribute("aria-current", "step");
    } else {
      step.removeAttribute("aria-current");
    }
  });

  if (stepNumber === 3) {
    renderReview();
  }

  document.querySelector(`[data-step="${stepNumber}"] h2`).focus();
}

function validateSelects(step) {
  const selects = [...step.querySelectorAll("select[required]")];
  const firstInvalid = selects.find((select) => !select.checkValidity());

  if (firstInvalid) {
    firstInvalid.reportValidity();
    return false;
  }
  return true;
}

function validateGroups(stepNumber) {
  const missingGroup = requiredGroups[stepNumber]?.find(
    (name) => !form.querySelector(`[name="${name}"]:checked`),
  );

  if (missingGroup) {
    showMessage("Please answer every required question before continuing.");
    form.querySelector(`[name="${missingGroup}"]`).focus();
    return false;
  }
  return true;
}

function validateExclusiveSelection(name, exclusiveValue, message) {
  const selections = selectedValues(name);
  if (selections.includes(exclusiveValue) && selections.length > 1) {
    showMessage(message);
    form.querySelector(`[name="${name}"][value="${exclusiveValue}"]`).focus();
    return false;
  }
  return true;
}

function validateProfileRelationships() {
  if (
    !validateExclusiveSelection(
      "available_equipment",
      "No equipment, bodyweight only",
      "Choose either No equipment or specific equipment, not both.",
    )
  ) {
    return false;
  }

  if (
    !validateExclusiveSelection(
      "preferred_activities",
      "No preference",
      "Choose either No preference or specific preferred activities, not both.",
    )
  ) {
    return false;
  }

  if (
    !validateExclusiveSelection(
      "disliked_activities",
      "No disliked activities",
      "Choose either No disliked activities or specific disliked activities, not both.",
    )
  ) {
    return false;
  }

  const preferred = new Set(selectedValues("preferred_activities"));
  const overlappingActivities = selectedValues("disliked_activities").filter(
    (activity) => preferred.has(activity),
  );

  if (overlappingActivities.length) {
    showMessage(
      `${overlappingActivities.join(", ")} cannot be both preferred and disliked.`,
    );
    form
      .querySelector(
        `[name="disliked_activities"][value="${overlappingActivities[0]}"]`,
      )
      .focus();
    return false;
  }

  return true;
}

function validateCurrentStep() {
  const step = form.querySelector(`[data-step="${currentStep}"]`);
  clearMessage();
  return (
    validateSelects(step) &&
    validateGroups(currentStep) &&
    (currentStep !== 1 || validateProfileRelationships())
  );
}

form.addEventListener("click", (event) => {
  const action = event.target.dataset.action;

  if (action === "next" && validateCurrentStep()) {
    showStep(currentStep + 1);
  }

  if (action === "back") {
    showStep(currentStep - 1);
  }
});

form.elements.primary_goal.addEventListener("change", syncAdditionalGoals);

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const confirmation = document.querySelector("#intensity-confirmation");
  if (
    !confirmation.hidden &&
    !form.elements.challenging_intensity_confirmed.checked
  ) {
    showMessage("Confirm the challenging-intensity warning before continuing.");
    form.elements.challenging_intensity_confirmed.focus();
    return;
  }

  clearMessage();
  planResult.hidden = true;
  generateButton.disabled = true;
  generateButton.textContent = "Generating...";

  try {
    const response = await fetch("/plans", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildPlanRequest()),
    });
    const result = await response.json();

    if (!response.ok) {
      showMessage(validationMessage(result.detail));
      return;
    }

    if (result.status === "generated") {
      renderGeneratedPlan(result);
    } else {
      renderStoppedResult(result);
    }
  } catch {
    showMessage(
      "The application could not reach the planner. Confirm the FastAPI server is running and try again.",
    );
  } finally {
    generateButton.disabled = false;
    generateButton.textContent = "Generate my plan";
  }
});

syncAdditionalGoals();
