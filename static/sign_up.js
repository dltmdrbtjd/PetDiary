function signUp() {
	const data = (new FormData(document.forms[0]))
	return fetch('/api/sign_up', {
		method:'POST',
		body:data
	}).then(response => {
		return response.json()
	})
	.then(result => {
		if (result.success) {
			window.location.href = './login'
		}
		else {
			alert('중복된 아이디입니다. 다시 작성해주세요')
			window.location.reload()
		}
	})
}

document.addEventListener('DOMContentLoaded', event => {
	const valid = Array(3).fill(false)
	const $form = document.getElementById('login-form')
	const $id = document.getElementsByName('user-id')[0]
	const $password = document.getElementsByName('user-password')[0]
	const $doubleCheck = document.getElementsByName('double-check')[0]

	function checkId() {
		const id = $id.value
		valid[0] = /\s/.test(id) || id < 8 ? false : true
	}
	function checkPassword() {
		const password = $password.value
		const $checkList = document.querySelectorAll('.check-list > li')

		// Set to default
		$checkList.forEach($li => {
			$li.style.color = 'red'
			$li.firstChild.textContent = '❌'
		})

		// 1. At least 8 letters
		if (/.{8}/.test(password)) {
			$checkList[0].style.color = 'green'
			$checkList[0].firstChild.textContent = '✔'
		}

		// 2. At least one uppercase letter
		if (/[A-Z]/.test(password)) {
			$checkList[1].style.color = 'green'
			$checkList[1].firstChild.textContent = '✔'
		}
		// 3. At least one lowercase letter
		if (/[a-z]/.test(password)) {
			$checkList[2].style.color = 'green'
			$checkList[2].firstChild.textContent = '✔'
		}
		// 4. At least one number
		if (/\d/.test(password)) {
			$checkList[3].style.color = 'green'
			$checkList[3].firstChild.textContent = '✔'
		}
		// 5. At leat one special character
		if (/[^A-Za-z0-9]/.test(password)) {
			$checkList[4].style.color = 'green'
			$checkList[4].firstChild.textContent = '✔'
		}
		// 6. No white space
		if (!/\s/.test(password)) {
			$checkList[5].style.color = 'green'
			$checkList[5].firstChild.textContent = '✔'
		}

		valid[1] = [...$checkList].every($li => $li.firstChild.textContent === '✔') ? true : false
	}
	function doubleCheckPassword() {
		valid[2] = $password.value === $doubleCheck.value ? true : false
	}
	function validate() {
		$button = document.getElementsByClassName('btn-primary')[0]
		$button.disabled = valid.every(e => e) ? false : true
	}
	checkPassword()
	$id.addEventListener('input', checkId)
	$password.addEventListener('input', checkPassword)
	$doubleCheck.addEventListener('input', doubleCheckPassword)
//aA123!@#
	$inputList = document.querySelectorAll('.mb-3 input')
	$inputList.forEach($input => {
		$input.addEventListener('input', validate)
	})
})
