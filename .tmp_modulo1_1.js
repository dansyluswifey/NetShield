
        const MODULE_ID = 'm1';
        const EXERCISES = [
            'Leer el material de aprendizaje del módulo',
            'Completar el simulador del banner de cookies',
            'Ver el ejemplo visual de cookies',
            'Guardar solo cookies esenciales'
        ];
        const TESTS = ['Quiz de comprensión'];
        const MAX_ATTEMPTS = 2;
        const QUIZ_CORRECT = { q1: 'a2', q2: 'a3', q3: 'a1', q4: 'a1', q5: 'a1' };

        function loadProgress() {
            try { return JSON.parse(localStorage.getItem('netshield_progress') || '{}'); } catch (e) { return {}; }
        }

        function saveProgress(data) {
            localStorage.setItem('netshield_progress', JSON.stringify(data));
        }

        function ensure(state) {
            if (!state[MODULE_ID]) {
                state[MODULE_ID] = { exercises: EXERCISES.map(() => false), tests: TESTS.map(() => false), answers: {}, attemptsRemaining: MAX_ATTEMPTS };
            }
            if (typeof state[MODULE_ID].attemptsRemaining !== 'number') {
                state[MODULE_ID].attemptsRemaining = MAX_ATTEMPTS;
            }
            if (!state[MODULE_ID].answers) {
                state[MODULE_ID].answers = {};
            }
        }

        function getState() {
            const state = loadProgress();
            ensure(state);
            return state;
        }

        function renderChecklist() {
            const state = getState();
            const exerciseList = document.getElementById('exercise-checklist');
            const testList = document.getElementById('test-checklist');
            exerciseList.innerHTML = '';
            testList.innerHTML = '';

            EXERCISES.forEach((text, index) => {
                const done = state[MODULE_ID].exercises[index];
                const label = document.createElement('label');
                label.className = 'list-item';
                label.innerHTML = `<input type="checkbox" ${done ? 'checked' : ''} disabled><span>${text}</span>`;
                exerciseList.appendChild(label);
            });

            const testDone = state[MODULE_ID].tests[0];
            const label = document.createElement('label');
            label.className = 'list-item';
            label.innerHTML = `<input type="checkbox" ${testDone ? 'checked' : ''} disabled><span>${TESTS[0]}</span>`;
            testList.appendChild(label);
            updateQuizUI();
        }

        function updateQuizUI() {
            const state = getState();
            document.querySelectorAll('.option-label').forEach(label => {
                const questionId = label.dataset.question;
                const optionId = label.dataset.option;
                label.classList.toggle('selected-option', state[MODULE_ID].answers[questionId] === optionId);
            });

            const info = document.getElementById('attempts-info');
            const button = document.getElementById('validate-quiz');
            const restartButton = document.getElementById('restart-module');
            if (state[MODULE_ID].tests[0]) {
                info.innerText = 'Prueba completada ✅';
                button.disabled = true;
                if (restartButton) restartButton.style.display = 'none';
            } else {
                info.innerText = `Intentos restantes: ${state[MODULE_ID].attemptsRemaining}`;
                button.disabled = state[MODULE_ID].attemptsRemaining <= 0;
                if (restartButton) {
                    restartButton.style.display = state[MODULE_ID].attemptsRemaining <= 0 ? 'inline-flex' : 'none';
                }
            }
        }

        function selectQuizOption(element, questionId, optionId) {
            const state = getState();
            state[MODULE_ID].answers[questionId] = optionId;
            saveProgress(state);
            document.querySelectorAll(`[data-question="${questionId}"]`).forEach(label => label.classList.remove('selected-option'));
            element.classList.add('selected-option');
        }

        function showQuizFeedback(message, background, color) {
            const feedback = document.getElementById('quiz-feedback');
            feedback.classList.remove('hidden');
            feedback.innerText = message;
            feedback.style.background = background;
            feedback.style.color = color;
        }

        function validateQuiz() {
            const state = getState();
            if (state[MODULE_ID].tests[0]) return;

            const answers = state[MODULE_ID].answers || {};
            const allAnswered = Object.keys(QUIZ_CORRECT).every(q => answers[q]);
            if (!allAnswered) {
                showQuizFeedback('Debes responder todas las preguntas antes de validar.', '#fde68a', '#92400e');
                return;
            }

            const wrong = Object.keys(QUIZ_CORRECT).filter(q => answers[q] !== QUIZ_CORRECT[q]);
            if (wrong.length === 0) {
                state[MODULE_ID].tests[0] = true;
                saveProgress(state);
                showQuizFeedback('✅ Todas las respuestas son correctas. Prueba completada.', '#dcfce7', '#15803d');
            } else {
                state[MODULE_ID].attemptsRemaining = Math.max(0, state[MODULE_ID].attemptsRemaining - 1);
                saveProgress(state);
                if (state[MODULE_ID].attemptsRemaining > 0) {
                    showQuizFeedback(`⚠️ Algunas respuestas son incorrectas. Te quedan ${state[MODULE_ID].attemptsRemaining} intentos.`, '#fee2e2', '#b91c1c');
                } else {
                    showQuizFeedback('❌ No quedan intentos. Usa el botón Reiniciar módulo para volver a intentarlo.', '#fee2e2', '#b91c1c');
                }
            }
            updateQuizUI();
        }

        function resetModule() {
            const state = getState();
            state[MODULE_ID].attemptsRemaining = MAX_ATTEMPTS;
            state[MODULE_ID].answers = {};
            state[MODULE_ID].tests[0] = false;
            state[MODULE_ID].exercises = EXERCISES.map(() => false);
            saveProgress(state);
            document.querySelectorAll('.option-label').forEach(label => label.classList.remove('selected-option', 'option-correct', 'option-wrong'));
            document.getElementById('quiz-feedback').classList.add('hidden');
            renderChecklist();
            updateQuizUI();
        }

        function resolveSimulator(action) {
            const feedback = document.getElementById('sim-feedback-box');
            const state = getState();
            state[MODULE_ID].exercises[1] = true;
            saveProgress(state);
            renderChecklist();
            feedback.classList.remove('hidden');
            if (action === 'accept') {
                feedback.innerText = '❌ Elegir aceptar todo entrega tu información a redes publicitarias y reduce tu control de tu información.';
                feedback.style.background = '#fee2e2';
                feedback.style.color = '#b91c1c';
            } else {
                feedback.innerText = '✅ Excelente. Configurar manualmente reduce el rastreo y mejora el control de tu información.';
                feedback.style.background = '#dcfce7';
                feedback.style.color = '#15803d';
            }
        }

        function markTheoryRead() {
            const state = getState();
            state[MODULE_ID].exercises[0] = true;
            saveProgress(state);
            renderChecklist();
        }

        function markVisualSeen() {
            const state = getState();
            state[MODULE_ID].exercises[2] = true;
            saveProgress(state);
            renderChecklist();
        }

        function applyCookiePreferences() {
            const analytics = document.getElementById('cookie-analytics').checked;
            const marketing = document.getElementById('cookie-marketing').checked;
            const feedback = document.getElementById('cookie-preference-feedback');
            const state = getState();
            if (!analytics && !marketing) {
                feedback.classList.remove('hidden');
                feedback.innerText = '✅ Buena elección. Solo cookies esenciales activas.';
                feedback.style.background = '#dcfce7';
                feedback.style.color = '#15803d';
                state[MODULE_ID].exercises[3] = true;
            } else {
                feedback.classList.remove('hidden');
                feedback.innerText = '⚠️ Aún hay cookies no esenciales activadas. Ajusta para mayor privacidad.';
                feedback.style.background = '#fee2e2';
                feedback.style.color = '#b91c1c';
                state[MODULE_ID].exercises[3] = false;
            }
            saveProgress(state);
            renderChecklist();
        }

        function markContentReviewed() {
            const state = getState();
            state[MODULE_ID].exercises[3] = true;
            saveProgress(state);
            renderChecklist();
        }

        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('validate-quiz').addEventListener('click', validateQuiz);
            document.getElementById('mark-theory').addEventListener('click', markTheoryRead);
            document.getElementById('mark-visual').addEventListener('click', markVisualSeen);
            renderChecklist();
        });
    