package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsInArray(t *testing.T) {
    // Test 1: Existing element in the array
    assert.True(t, IsInArray([]string{"i", "like", "go", "!"}, "go"))

    // Test 2: Non-existing element in the array
    assert.False(t, IsInArray([]string{"i", "like", "go", "!"}, "rust"))

    // Test 3: Empty array, should return false for any search
    assert.False(t, IsInArray([]string{}, "any"))

    // Test 4: Element is at the beginning of the array
    assert.True(t, IsInArray([]string{"first", "second", "third"}, "first"))

    // Test 5: Element is at the end of the array
    assert.True(t, IsInArray([]string{"first", "second", "third"}, "third"))

    // Test 6: Array with duplicate values, should return true if value is present
    assert.True(t, IsInArray([]string{"apple", "banana", "apple", "cherry"}, "apple"))

    // Test 7: Case sensitivity check, should return false if the case doesn't match
    assert.False(t, IsInArray([]string{"Hello", "world"}, "hello"))

    // Test 8: Single element array, should return true if the element matches
    assert.True(t, IsInArray([]string{"single"}, "single"))

    // Test 9: Single element array, should return false if the element doesn't match
    assert.False(t, IsInArray([]string{"single"}, "notfound"))

    // Test 10: Special characters in the array, should return true if the value is found
    assert.True(t, IsInArray([]string{"$apple", "@banana", "#cherry"}, "@banana"))
}


func TestTransformUserReply_BasicReplacement(t *testing.T) {
    // Test Case 1: Basic replacement of "@person" with a formatted user mention.
    // Input: "Howdy, @person! :wave:"
    // Expected Output: "Howdy, <@U12345678>! :wave:"
    assert.Equal(t, "Howdy, <@U12345678>! :wave:", TransformUserReply("Howdy, @person! :wave:", "U12345678"))
}

func TestTransformUserReply_MixedCasePlaceholder(t *testing.T) {
    // Test Case 2: Placeholder with mixed case ("@person") should not be replaced.
    // Input: "Hello, @person! How are you?"
    // Expected Output: "Hello, <@U12345678>! How are you?"
    assert.Equal(t, "Hello, <@U12345678>! How are you?", TransformUserReply("Hello, @person! How are you?", "U12345678"))
}

func TestTransformUserReply_Placeholders(t *testing.T) {
    // Test Case 3: Two Placeholder 
    // Input: "Good morning, @person! Have a nice day @person."
    // Expected Output: "Good morning, <@U12345678>! Have a nice day <@U12345678>."
    assert.Equal(t, "Good morning, <@U12345678>! Have a nice day <@U12345678>.", TransformUserReply("Good morning, @person! Have a nice day @person.", "U12345678"))
}

func TestTransformUserReply_onlyplaceholder(t *testing.T) {
    // Test Case 4: only placeholder
    // Input: "@person"
    // Expected Output: "<@U12345678>"
    assert.Equal(t, "<@U12345678>", TransformUserReply("@person", "U12345678"))
}

func TestTransformUserReply_EmptyInput(t *testing.T) {
    // Test Case 5: Empty input string should return an empty string, as no transformation is needed.
    // Input: ""
    // Expected Output: ""
    assert.Equal(t, "", TransformUserReply("", "U12345678"))
}
